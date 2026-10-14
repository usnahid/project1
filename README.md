# RoadGuard AI — Smart Road Damage Detection and Reporting Platform

> **"Detect. Report. Repair."**  
> An end-to-end civic-tech platform that empowers citizens to report road hazards (potholes, cracks, broken edges, damaged manholes) via photograph uploads, analyzes severity through computer vision, flags duplicate reports using geospatial proximity, and streamlines municipal repair workflows.

---

## 🌟 Key Highlights & Features

1. **AI-Powered Damage Detection & Severity Triage**
   - **Real Computer Vision Model:** Computes multi-pass spatial metrics using Pillow (pixel luminance distributions, dark cavity void ratios for potholes, high-pass edge gradients for cracks, and local standard deviation for surface aggregate wear).
   - **Transparent Confidence & Severity:** Generates empirical confidence scores and estimates urgency as **Low**, **Medium**, or **High** with full reasoning diagnostics.
   - **Demo Simulator Toggle:** Clearly disclosed toggle for presentations and deterministic testing when camera/network conditions require offline reliability. Never claims simulated outputs are neural network predictions.
   - **Manual Citizen Override:** Citizens can easily review and adjust categories or severity ratings before submission.

2. **Geospatial Proximity Duplicate Prevention**
   - Implements the **Haversine great-circle formula** to evaluate distance against existing reports.
   - Automatically detects and flags submissions within **50 meters** of active road issues.
   - Displays real-time warnings to citizens before submission and allows administrators to review, link, or dismiss duplicate tickets.

3. **Interactive Live Damage Map**
   - Built with **React Leaflet** and **OpenStreetMap**.
   - Custom colored pins for severity: 🔴 **Red (High)**, 🟡 **Amber (Medium)**, 🟢 **Green (Low)**.
   - Rich interactive popups featuring image previews, report ID, severity badge, status badge, road name, and one-click detail navigation.
   - Split layout with list view alongside the map and instant zoom-to-marker focus.

4. **Public Citizen Tracking Portal**
   - Searchable, sortable incident registry with multi-criteria filtering (status, severity, category).
   - **Instant Report ID Lookup:** Track progress by entering unique codes (e.g., `RG-2026-1001`).
   - Demo citizen persona switcher to simulate citizen accounts without requiring paid authentication.

5. **Administrative Operations & Dispatch Console**
   - Operational KPI counters: Total Reports, Under Review, Active Repairs, Resolved, Duplicates Flagged.
   - **Interactive Analytics Visualizations with Recharts:**
     - Defects by Severity (Pie Chart)
     - Reports by Category (Bar Chart)
     - Incident Pipeline (Horizontal Bar Chart)
   - **Full Incident Management Drawer:**
     - Multi-stage lifecycle progression: `Submitted` → `Under Review` → `Assigned` → `In Progress` → `Resolved` (or `Rejected` with required reason).
     - Maintenance crew assignment (e.g., *Rapid Asphalt Response Team - Zone 3*, *Municipal Drainage & Manhole Unit*).
     - Internal dispatch notes and immutable timestamped status audit trail.

---

## 🏗️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons |
| **Mapping & Geospatial** | Leaflet, React Leaflet, OpenStreetMap Tiles |
| **Analytics & Data Viz** | Recharts (Pie, Bar, Area charts) |
| **Backend API** | Python 3.12, FastAPI, Uvicorn, Pydantic v2 |
| **Database** | SQLite (WAL mode, Foreign Keys, Indexes, Data-Access Layer) |
| **Vision & Image Processing** | Pillow (PIL) Computer Vision Heuristic Classifier, Multipart Uploads |
| **Geospatial Algorithm** | Haversine Great-Circle Distance |

---

## 📁 Repository Structure

```
Road damage detector/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application & REST endpoints
│   │   ├── config.py            # Configuration settings & paths
│   │   ├── database.py          # SQLite schema, queries & analytics
│   │   ├── models.py            # Database models
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── ai_service.py        # Modular AI: CV Heuristic & Demo Simulator
│   │   ├── duplicate_service.py # Haversine distance duplicate detection
│   │   └── seed_data.py         # Realistic demo seed reports & image generator
│   ├── uploads/                 # Stored incident images & generated samples
│   ├── requirements.txt         # Backend Python dependencies
│   └── run.py                   # Backend entrypoint runner script
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx             # Navigation header & demo data reset
│   │   │   ├── Footer.tsx             # Civic disclaimer & footer links
│   │   │   ├── MapView.tsx            # Leaflet map with custom colored SVG pins
│   │   │   ├── StatCard.tsx           # Metric cards
│   │   │   ├── StatusBadge.tsx        # Workflow status badges
│   │   │   ├── SeverityBadge.tsx      # Low/Medium/High severity badges
│   │   │   └── DuplicateAlertModal.tsx# Proximity duplicate warning dialog
│   │   ├── pages/
│   │   │   ├── LandingPage.tsx        # Hero, 3-step guide, recent reports
│   │   │   ├── ReportDamagePage.tsx   # 5-step reporting flow with AI analysis
│   │   │   ├── LiveMapPage.tsx        # Geospatial interactive map & list
│   │   │   ├── CitizenDashboardPage.tsx # Tracking portal & ID search
│   │   │   ├── AdminDashboardPage.tsx # Ops console, charts & status triage
│   │   │   ├── ReportDetailsPage.tsx  # Detailed report view & audit timeline
│   │   │   └── AboutPage.tsx          # Architecture & transparency disclosures
│   │   ├── services/
│   │   │   └── api.ts                 # Typed REST client
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript data models
│   │   ├── App.tsx                    # Route manager with hash synchronization
│   │   ├── index.css                  # Tailwind & Leaflet styles
│   │   └── main.tsx                   # React mount entrypoint
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts                 # Vite config with backend proxy
│   └── tsconfig.json
├── test_e2e.py                        # Automated end-to-end integration test suite
├── .gitignore
├── .env.example
└── README.md
```

---

## 🚀 Quickstart & Installation

### Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- **Node.js 18+** & **npm**

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI backend server (runs on http://127.0.0.1:8000)
python run.py
```
*The backend will automatically initialize SQLite tables, generate sample textured road damage images, and seed realistic demo reports on first startup.*

### 2. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server (runs on http://localhost:5173)
npm run dev
```

Visit **`http://localhost:5173`** in your browser to launch RoadGuard AI!

---

## 📡 Backend API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check & SQLite status |
| `GET` | `/api/analytics` | Aggregated metrics for charts and dashboards |
| `GET` | `/api/map/reports` | Public geolocated reports (omits private contact info) |
| `GET` | `/api/reports` | List reports with filtering by status, severity, category, search |
| `POST` | `/api/reports` | Submit a new damage report with photo & metadata |
| `GET` | `/api/reports/{id}` | Full report details with audit history & admin notes |
| `PATCH` | `/api/reports/{id}` | Update editable report attributes |
| `POST` | `/api/analyze` | AI image analysis (returns category, severity, confidence, metrics) |
| `POST` | `/api/reports/check-duplicate` | Haversine proximity duplicate check (50m radius) |
| `POST` | `/api/reports/{id}/status` | Update workflow status (`Under Review`, `Assigned`, `In Progress`, `Resolved`, `Rejected`) |
| `POST` | `/api/reports/{id}/notes` | Add internal municipal officer note |
| `POST` | `/api/reset-demo` | Reset database to clean realistic seed records |

---

## 🧪 Automated Testing

Run the included end-to-end integration test suite against the running API:
```bash
python test_e2e.py
```
Tests all 10 core integration flows:
- Health check verification
- Analytics calculations
- Public map privacy verification (ensures contact numbers are redacted)
- Computer Vision heuristic image analysis
- Haversine proximity duplicate detection
- Full report submission
- Chronological status transition workflow
- Internal admin notes persistence
- Real-time analytics recalculation

---

## 🏆 Live Hackathon Demonstration Flow (2 Minutes)

1. **Landing Page:** Open `http://localhost:5173` and highlight the live statistics counters and the 3-step civic workflow.
2. **Report Road Damage:** Click **"Report Road Damage"**.
   - Use the 1-click **"Severe Pothole"** sample image or upload a custom road photo.
   - Click **"Next: Analyze Image"** to trigger the AI analysis. Observe the computer vision feature metrics (dark cavity void ratio, edge density, confidence score).
   - Click **"Next: Set Location"**. Pick a preset landmark (e.g. *Cyber Towers Junction*) or click on the interactive map. Notice the instant duplicate warning alert if clicked near existing reports!
   - Fill in details and click **"Submit Road Damage Report"**.
3. **Confirmation:** Observe the unique generated Report ID (e.g., `RG-2026-XXXX`).
4. **Live Map:** Click **"Locate on Live Map"** to see the colored severity marker positioned on OpenStreetMap with its interactive popup.
5. **Admin Operations:** Navigate to **"Admin Console"**:
   - Inspect the Recharts distribution graphs.
   - Open your submitted report in the triage queue.
   - Advance the status to **"Assigned"** and select the *Rapid Asphalt Response Team*.
   - Mark as **"In Progress"**, then **"Resolved"**.
   - Inspect the timestamped chronological audit trail and internal notes.
6. **Reset:** Click the top navbar **"Reset Data"** button anytime to restore a clean demo slate.

---

## ⚖️ Civic Disclaimer
RoadGuard AI is developed as an open civic-tech demonstration platform. Reports submitted in this MVP are recorded in a demonstration database and do not represent legally binding municipal service requests unless integrated with an authorized city authority API.
