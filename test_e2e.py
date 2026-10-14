import urllib.request
import urllib.parse
import json
import mimetypes
import uuid
import sys
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def post_json(path, data):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def post_multipart(path, fields, file_field_name, file_path):
    boundary = uuid.uuid4().hex
    data = []
    
    for name, value in fields.items():
        data.append(f"--{boundary}".encode())
        data.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        data.append(b"")
        data.append(str(value).encode())
        
    if file_path and Path(file_path).exists():
        fname = Path(file_path).name
        data.append(f"--{boundary}".encode())
        data.append(f'Content-Disposition: form-data; name="{file_field_name}"; filename="{fname}"'.encode())
        data.append(b"Content-Type: image/jpeg")
        data.append(b"")
        with open(file_path, "rb") as f:
            data.append(f.read())
            
    data.append(f"--{boundary}--".encode())
    data.append(b"")
    body = b"\r\n".join(data)
    
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def run_tests():
    print("=== STARTING ROADGUARD AI END-TO-END INTEGRATION TEST ===")
    
    # 1. Health check
    print("\n[Test 1] Health Check...")
    h = get("/api/health")
    assert h["status"] == "healthy", "Health check failed"
    print(f"[PASS] Health OK: {h['app']} v{h['version']}")
    
    # 2. Analytics
    print("\n[Test 2] Analytics Check...")
    an = get("/api/analytics")
    assert an["total_reports"] >= 10, "Expected at least 10 sample reports"
    print(f"[PASS] Analytics OK: {an['total_reports']} reports, {an['resolved_reports']} resolved, {an['high_severity_reports']} high severity")
    
    # 3. Public Map
    print("\n[Test 3] Public Map Reports...")
    map_reports = get("/api/map/reports")
    assert len(map_reports) > 0, "Map reports empty"
    for r in map_reports:
        assert "reporter_contact" not in r, "Privacy violation: reporter_contact exposed in public map"
    print(f"[PASS] Public Map OK: {len(map_reports)} geolocated reports, private contact info verified omitted")
    
    # 4. AI Image Analysis (Real CV heuristic mode)
    print("\n[Test 4] AI Image Analysis (Real CV Heuristic)...")
    sample_img = Path("backend/uploads/sample_pothole_rg-2026-1001.jpg")
    analysis = post_multipart("/api/analyze", {"demo_mode": "false"}, "file", sample_img)
    assert analysis["predicted_category"] == "Pothole", f"Expected Pothole, got {analysis['predicted_category']}"
    assert analysis["analysis_mode"] == "cv_heuristic_model"
    assert "edge_density" in analysis["features_detected"]
    print(f"[PASS] Real CV Analysis OK: Detected '{analysis['predicted_category']}', Severity: {analysis['severity']}, Confidence: {analysis['confidence']}, Mode: {analysis['analysis_mode']}")
    
    # 5. Duplicate Check
    print("\n[Test 5] Proximity Duplicate Detection...")
    dup_res = post_json("/api/reports/check-duplicate", {
        "latitude": 17.4504,
        "longitude": 78.3808,
        "category": "Pothole",
        "radius_meters": 50.0
    })
    assert dup_res["is_potential_duplicate"] is True, "Failed to detect known duplicate at Cyber Towers"
    print(f"[PASS] Duplicate Detection OK: {dup_res['message']}")
    
    # 6. Report Submission
    print("\n[Test 6] Submit New Road Damage Report...")
    new_rep = post_multipart("/api/reports", {
        "predicted_category": "Pothole",
        "confirmed_category": "Pothole",
        "severity": "High",
        "confidence": "0.95",
        "analysis_mode": "cv_heuristic_model",
        "description": "Critical asphalt hole spotted during test drive near Cyber Towers.",
        "road_name": "Hitech City Test Corridor",
        "landmark": "Opposite Metro Pillar 1045",
        "latitude": "17.45042",
        "longitude": "78.38081",
        "reporter_name": "Aditya Sharma",
        "reporter_contact": "+91 99887 76655",
        "force_submit_duplicate": "true"
    }, "image", sample_img)
    rep_id = new_rep["report_id"]
    assert rep_id.startswith("RG-2026-"), f"Unexpected ID format {rep_id}"
    print(f"[PASS] New Report Created OK: ID={rep_id}, Status={new_rep['status']}, Flagged Duplicate={new_rep['is_potential_duplicate']}")
    
    # 7. Fetch Details
    print(f"\n[Test 7] Fetch Report Details for {rep_id}...")
    details = get(f"/api/reports/{rep_id}")
    assert details["report_id"] == rep_id
    assert len(details["status_history"]) >= 1
    print(f"[PASS] Report Details OK: Category={details['confirmed_category']}, History count={len(details['status_history'])}")
    
    # 8. Status Workflow Transitions
    print(f"\n[Test 8] Workflow Transitions (Submitted -> Under Review -> Assigned -> In Progress -> Resolved)...")
    st1 = post_json(f"/api/reports/{rep_id}/status", {"status": "Under Review", "note": "Dispatcher reviewed photo"})
    assert st1["status"] == "Under Review"
    
    st2 = post_json(f"/api/reports/{rep_id}/status", {"status": "Assigned", "assigned_team": "Rapid Asphalt Response Team - Zone 3"})
    assert st2["status"] == "Assigned"
    assert st2["assigned_team"] == "Rapid Asphalt Response Team - Zone 3"
    
    st3 = post_json(f"/api/reports/{rep_id}/status", {"status": "In Progress", "note": "Asphalt patch truck dispatched to site"})
    assert st3["status"] == "In Progress"
    
    st4 = post_json(f"/api/reports/{rep_id}/status", {"status": "Resolved", "note": "Pothole filled and rolled. Repaired successfully."})
    assert st4["status"] == "Resolved"
    assert st4["resolved_at"] is not None
    print(f"[PASS] Status Workflow OK: Full lifecycle progression successfully stored in audit history")
    
    # 9. Admin Notes
    print(f"\n[Test 9] Add Internal Admin Note...")
    note_res = post_json(f"/api/reports/{rep_id}/notes", {"note": "Quality inspector verified cold-mix compaction passed."})
    assert len(note_res["admin_notes"]) >= 1
    print(f"[PASS] Admin Notes OK: {note_res['admin_notes'][0]['note']}")
    
    # 10. Re-verify Analytics
    print("\n[Test 10] Updated Analytics...")
    an2 = get("/api/analytics")
    assert an2["total_reports"] == an["total_reports"] + 1
    print(f"[PASS] Analytics Updated OK: Total is now {an2['total_reports']}, Resolved is {an2['resolved_reports']}")
    
    print("\n=======================================================")
    print("ALL 10 END-TO-END INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
