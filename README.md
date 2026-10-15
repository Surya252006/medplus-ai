# MedPulse AI — Rural Healthcare Triage & Resource Navigator

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.143-teal.svg)](https://fastapi.tiangolo.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-green.svg)](https://leafletjs.com/)
[![OpenStreetMap](https://img.shields.io/badge/Maps-OpenStreetMap-brightgreen.svg)](https://www.openstreetmap.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> **Core Mission:** Make healthcare easier to access, understand, and navigate for rural and semi-urban communities, regardless of language, distance, or digital literacy.

---

## 1. Hackathon Pitch & Executive Summary

### The Problem
In rural and semi-urban regions across India and developing nations, millions of families face a dual healthcare breakdown:
1. **Delayed Critical Emergencies:** Patients experiencing subtle heart attack signs, venomous snakebites, or childhood respiratory distress delay seeking hospital care due to uncertainty, resulting in preventable mortality.
2. **Overburdened Secondary & Tertiary Hospitals:** Taluk and District hospitals are overwhelmed with mild, routine conditions (viral colds, tension headaches) because patients do not know whether their local Primary Health Centre (PHC) or Village Sub-Centre is equipped to treat them.
3. **Language & Literacy Barriers:** Most digital health apps are text-heavy, English-centric, and complex for rural elders or low-literacy citizens.

### The Innovation: MedPulse AI
**MedPulse AI** acts as a trustworthy digital first-responder and healthcare navigator:
- **Voice-First Multilingual Reporting:** Patients describe symptoms naturally using the Web Speech API in **Tamil (தமிழ்)**, **Hindi (हिन्दी)**, or **English**, with immediate text-fallback.
- **Safety-First Clinical Triage Engine:** Priority-1 clinical red flags (cardiac, stroke FAST criteria, hemorrhage, envenomation, severe respiratory distress) trigger instant emergency guidance (`108` / `112`), bypassing any delays.
- **Transparent Clinician Summaries:** Generates editable, structured clinical notes with chief complaints, durations, and pertinent negatives (e.g., missing vitals, allergy status) for doctors and ASHA community health workers.
- **Interactive Rural Healthcare Navigator:** Integrates OpenStreetMap and Leaflet to locate verified Primary Health Centres, Community Health Centres (CHC), and Taluk Hospitals with real-world travel directions, doctor availability, and 24/7 emergency indicators.
- **Zero Mandatory Registration & Privacy Safeguards:** Completely usable without login. No Protected Health Information (PHI) is logged, and users have single-click data purge controls.

### Social Impact
- **Saves Golden Hour in Emergencies:** Directs chest pain or stroke symptoms to emergency care with single-tap ambulance dialers.
- **Empowers ASHA Community Workers:** Provides frontline health workers with a clinical triage companion on low-cost smartphones.
- **Optimizes Public Health Capacity:** Steers routine cases to Primary Health Centres while conserving hospital beds for urgent traumas and emergencies.

---

## 2. Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Custom Healthcare Design System with Teal `#0D9488`, Soft Blue `#0284C7`, Slate `#0F172A`), Vanilla JavaScript (ES6+ modular), `@media print` 1-page clinical triage handoff slips |
| **Voice / Speech** | Browser Web Speech API (`webkitSpeechRecognition` & `speechSynthesis`) supporting `ta-IN`, `hi-IN`, and `en-IN` locales for both voice input and audio readout of triage guidance |
| **Mapping & GIS** | Leaflet.js (v1.9.4) with OpenStreetMap tiles, custom SVG category pins, Haversine proximity distance calculations |
| **Backend** | Python 3.13, FastAPI (ASGI async architecture), Uvicorn |
| **Validation & Schema** | Pydantic v2 schemas for all requests and responses |
| **NLP & Triage** | High-precision transparent multilingual medical lexicon & rule-based clinical decision protocol (Cardio, Stroke, Resp, Hemorrhagic, Tox/Rabies, Obstetric, Pediatric, Burns) with natural conversational duration parsing |
| **Database** | SQLite (with zero-PHI logging and schema mapped for MongoDB / PostgreSQL migration) |

---

## 3. Project Structure

```
medpulse-ai/
├── backend/
│   ├── main.py                   # FastAPI app, routing, CORS, static file serving
│   ├── schemas.py                # Pydantic request & response models
│   ├── triage_engine.py          # Validated clinical triage rules (Emergency, Urgent, Routine)
│   ├── translation_service.py    # Multilingual lexicon (Tamil, Hindi, English)
│   ├── summary_service.py        # Structured medical summary generator with pertinent negatives
│   ├── facility_service.py       # OpenStreetMap facility search & Haversine distance engine
│   ├── database.py               # SQLite persistence, demo seeds, and privacy controls
│   ├── requirements.txt          # Backend dependencies
│   └── .env.example              # Environment variables template
├── frontend/
│   ├── index.html                # Landing page & social impact presentation
│   ├── assessment.html           # Symptom assessment with voice input & triage cards
│   ├── facilities.html           # Leaflet map & healthcare facility resource finder
│   ├── dashboard.html            # Patient personal dashboard & privacy controls
│   ├── clinician.html            # Healthcare professional & ASHA review portal
│   ├── css/
│   │   ├── styles.css            # Calm, accessible healthcare design system
│   │   └── responsive.css        # Mobile, tablet, and touch-screen optimizations
│   └── js/
│       ├── api.js                # Centralized async API client & toast notifications
│       ├── app.js                # Global i18n dictionary (en, ta, hi) & navigation
│       ├── triage.js             # Voice recognition & assessment controller
│       └── facilities.js         # Leaflet OpenStreetMap controller with GPS
├── data/
│   └── sample_facilities.json    # Authentic rural Tamil Nadu healthcare facilities
└── README.md
```

---

## 4. Quick Start & Installation

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Modern web browser (Chrome, Edge, Firefox, Safari)

### Step 1: Clone & Setup Virtual Environment
```powershell
# Navigate to the workspace
cd d:\projects\dsu

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows Command Prompt:
.\venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Run the Automated Test Suite (11 Test Suites)
```powershell
$env:PYTHONIOENCODING="utf-8"
python backend/test_api.py
```

### Step 4: Run the Application
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to:
- **Landing Page:** [http://localhost:8000/](http://localhost:8000/)
- **Symptom Assessment:** [http://localhost:8000/assessment](http://localhost:8000/assessment)
- **Healthcare Navigator:** [http://localhost:8000/facilities](http://localhost:8000/facilities)
- **Patient Dashboard:** [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
- **Clinician Portal:** [http://localhost:8000/clinician](http://localhost:8000/clinician)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 5. API Reference Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check, module statuses, and database state |
| `GET` | `/api/languages` | Supported languages metadata (en, ta, hi) |
| `POST` | `/api/triage` | Safety-first clinical urgency triage assessment |
| `POST` | `/api/translate` | Multilingual medical normalization & concept extraction |
| `POST` | `/api/summary` | Structured clinical note with pertinent negatives |
| `GET` | `/api/facilities` | Filter healthcare facilities by text, category, emergency, and GPS distance |
| `GET` | `/api/facilities/{id}` | Detailed facility information |
| `GET` | `/api/assessments` | Retrieve saved assessment history |
| `DELETE` | `/api/assessments/{id}`| Permanently delete a single assessment record |
| `DELETE` | `/api/assessments` | Purge entire patient assessment history (Privacy action) |
| `GET` | `/api/clinician/queue`| Clinician triage queue sorted by urgency (Emergency first) |
| `POST` | `/api/clinician/acknowledge` | Clinician review sign-off and clinical notes |

---

## 6. Hackathon Demonstration Walkthrough

1. **Landing Page:**
   - Open `http://localhost:8000/`.
   - Toggle language to **தமிழ் (Tamil)** or **हिन्दी (Hindi)** to see real-time UI localization.
   - Note the persistent emergency hotline banner with click-to-dial `108` and `112`.
2. **Symptom Assessment (Voice & Multilingual):**
   - Click **"Check My Symptoms"**.
   - Click on the sample prompt chip: `🚨 தமிழ்: நெஞ்சு வலி (Emergency)` or speak into the microphone.
   - Click **"Assess Care Urgency"**.
   - Watch the dedicated **EMERGENCY (Red)** card render with immediate 108 ambulance instructions.
   - Inspect the **Structured Medical Summary for Healthcare Provider** with identified pertinent negatives and editable fields.
3. **Healthcare Resource Navigator:**
   - Click **"Find Matching Facilities"** or navigate to `http://localhost:8000/facilities`.
   - Filter by **Hospitals** or check **"Only show facilities with 24/7 Emergency Care"**.
   - Click **"📍 Use My Location"** to compute real-time Haversine distance in kilometers.
   - Click any facility card (e.g., *Melur Government Taluk Hospital*) to smoothly fly the Leaflet map to the marker.
4. **Patient Dashboard & Privacy Controls:**
   - Open `http://localhost:8000/dashboard` to view recent assessments and urgency breakdowns.
   - Click **"Delete All History"** to verify privacy-first zero-retention capability.
5. **Healthcare Professional / Clinician Portal:**
   - Open `http://localhost:8000/clinician` to view the emergency queue.
   - Type doctor's clinical orders into the notes input and click **"Acknowledge & Sign Off"**.

---

## 7. Safety, Clinical Limitations & Ethics

> [!IMPORTANT]
> - **Preliminary Guidance Only:** MedPulse AI is designed strictly as a clinical decision support and health navigation tool. It **does NOT diagnose diseases, prescribe medication, or replace a licensed physician**.
> - **Never Delay Emergency Care:** Emergency red flags are rule-validated and triggered before any secondary NLP analysis.
> - **Demonstration Facility Data:** The healthcare directory uses verified representative facilities from rural Tamil Nadu for demonstration purposes.

---

## 8. License & Acknowledgments

Distributed under the MIT License. Developed for the National Level Healthcare Hackathon. Built with dedication to improving rural healthcare accessibility.
