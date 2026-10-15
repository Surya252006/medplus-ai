import os
import time
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .schemas import (
    LanguageOption, TriageRequest, TriageResponse,
    TranslationRequest, TranslationResponse,
    MedicalSummaryRequest, MedicalSummaryResponse,
    FacilityItem, FacilityListResponse,
    SavedAssessment, ClinicianAcknowledgeRequest
)
from .triage_engine import triage_engine
from .translation_service import translation_service, SUPPORTED_LANGUAGES
from .summary_service import generate_medical_summary
from .facility_service import facility_service
from .database import (
    init_db, save_assessment, get_assessments,
    get_assessment_by_id, delete_assessment,
    delete_all_assessments, acknowledge_assessment,
    seed_demo_assessments
)

# Safe logging setup (Strictly excludes Protected Health Information / narratives)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] medpulse: %(message)s"
)
logger = logging.getLogger("medpulse")

# Initialize SQLite database
init_db()
seed_demo_assessments()

app = FastAPI(
    title="MedPulse AI — Rural Healthcare Triage & Resource Navigator",
    description="Accessible AI-assisted clinical triage, multilingual symptom reporting, and rural healthcare resource navigator.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()

# 1. Health check
@app.get("/api/health", tags=["System"])
def health_check():
    uptime_seconds = round(time.time() - START_TIME, 1)
    return {
        "status": "healthy",
        "service": "MedPulse AI Backend",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "database": "SQLite (Active)",
        "modules": {
            "triage_engine": "Rule-Based Clinical Triage (Validated)",
            "translation_service": "Multilingual Medical Lexicon (Active)",
            "facility_service": "OpenStreetMap Regional Directory (Active)",
            "privacy_guard": "Strict Zero-PHI Logging (Active)"
        }
    }

# 2. Supported languages
@app.get("/api/languages", response_model=List[LanguageOption], tags=["Multilingual"])
def get_languages():
    return SUPPORTED_LANGUAGES

# 3. Translation & Normalization
@app.post("/api/translate", response_model=TranslationResponse, tags=["Multilingual"])
def translate_text(req: TranslationRequest):
    normalized, detected, identified = translation_service.translate_and_normalize(
        req.text, req.source_lang
    )
    logger.info(f"Translation request processed: lang={identified}, detected_terms={len(detected)}")
    return TranslationResponse(
        original_text=req.text,
        translated_text=normalized,
        source_lang=identified,
        target_lang="en",
        confidence=0.95 if detected else 0.85,
        detected_terms=detected
    )

# 4. Preliminary Clinical Triage
@app.post("/api/triage", response_model=TriageResponse, tags=["Triage"])
def process_triage(req: TriageRequest):
    logger.info(f"Triage initiated: lang={req.language}, age={req.age_group}, duration={req.duration}")
    
    triage_result = triage_engine.evaluate(req)
    
    # Save to history ONLY if user explicitly consented
    assessment_id = None
    if req.save_to_history:
        summary_req = MedicalSummaryRequest(
            symptoms_text=req.symptoms_text,
            translated_text=triage_result.translated_symptoms,
            language=req.language,
            age_group=req.age_group,
            duration=req.duration,
            additional_context=req.additional_context,
            urgency_category=triage_result.urgency_category,
            recognized_symptoms=triage_result.recognized_symptoms,
            red_flags_detected=triage_result.red_flags_detected,
            recommended_action=triage_result.recommended_action,
            recommended_facility_type=triage_result.recommended_facility_type
        )
        medical_summary = generate_medical_summary(summary_req)
        
        summary_text_val = medical_summary.clinical_rationale
        if triage_result.translated_symptoms and req.language != "en":
            summary_text_val += f" | Clinical Translation: {triage_result.translated_symptoms}"

        assessment_id = save_assessment(
            symptoms_original=req.symptoms_text,
            language=req.language,
            age_group=req.age_group or "adult",
            duration=req.duration or "",
            urgency_category=triage_result.urgency_category,
            urgency_color=triage_result.urgency_color,
            recommended_facility_type=triage_result.recommended_facility_type,
            summary_text=summary_text_val
        )
        triage_result.assessment_id = assessment_id
        logger.info(f"Assessment saved to user history with ID: {assessment_id}")

    logger.info(f"Triage completed: category={triage_result.urgency_category}, confidence={triage_result.confidence_score}")
    return triage_result

# 5. Structured Medical Summary
@app.post("/api/summary", response_model=MedicalSummaryResponse, tags=["Summary"])
def create_medical_summary(req: MedicalSummaryRequest):
    logger.info(f"Medical summary requested for urgency={req.urgency_category}")
    return generate_medical_summary(req)

# 6. Healthcare Facilities Directory & Proximity Search
@app.get("/api/facilities", response_model=FacilityListResponse, tags=["Facilities"])
def get_facilities(
    query: Optional[str] = Query(None, description="Village, town, district, or pin code"),
    category: Optional[str] = Query(None, description="Facility category: HOSPITAL, CHC, PHC, CLINIC"),
    emergency_only: bool = Query(False, description="Filter only facilities with 24/7 emergency care"),
    lat: Optional[float] = Query(None, description="User latitude"),
    lon: Optional[float] = Query(None, description="User longitude"),
    max_distance_km: Optional[float] = Query(None, description="Maximum distance in km")
):
    return facility_service.get_facilities(
        query=query,
        category=category,
        emergency_only=emergency_only,
        lat=lat,
        lon=lon,
        max_distance_km=max_distance_km
    )

@app.get("/api/facilities/{facility_id}", response_model=FacilityItem, tags=["Facilities"])
def get_facility_detail(facility_id: str):
    fac = facility_service.get_facility_by_id(facility_id)
    if not fac:
        raise HTTPException(status_code=404, detail="Healthcare facility not found")
    return fac

# 7. Saved Assessments (Opt-in Patient History)
@app.get("/api/assessments", response_model=List[SavedAssessment], tags=["History & Privacy"])
def list_assessments(limit: int = 50):
    return get_assessments(limit=limit)

@app.get("/api/assessments/{assessment_id}", response_model=SavedAssessment, tags=["History & Privacy"])
def retrieve_assessment(assessment_id: str):
    record = get_assessment_by_id(assessment_id)
    if not record:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return record

@app.delete("/api/assessments/{assessment_id}", tags=["History & Privacy"])
def remove_assessment(assessment_id: str):
    success = delete_assessment(assessment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Assessment not found or already deleted")
    logger.info(f"Assessment {assessment_id} deleted upon user request")
    return {"status": "success", "message": f"Assessment {assessment_id} permanently deleted"}

@app.delete("/api/assessments", tags=["History & Privacy"])
def clear_all_history():
    count = delete_all_assessments()
    logger.info(f"All patient history purged. Deleted {count} records.")
    return {"status": "success", "message": f"Successfully deleted {count} stored assessments"}

# 8. Healthcare Professional (Clinician / ASHA) View
@app.get("/api/clinician/queue", response_model=List[SavedAssessment], tags=["Clinician View"])
def clinician_queue():
    assessments = get_assessments(limit=100)
    # Sort: Emergency first, then Urgent, then Routine
    urgency_rank = {"EMERGENCY": 0, "URGENT": 1, "ROUTINE": 2}
    sorted_queue = sorted(
        assessments,
        key=lambda x: (x.get("clinician_acknowledged", False), urgency_rank.get(x.get("urgency_category", "ROUTINE"), 3))
    )
    return sorted_queue

@app.post("/api/clinician/acknowledge", tags=["Clinician View"])
def clinician_acknowledge(req: ClinicianAcknowledgeRequest):
    success = acknowledge_assessment(req.assessment_id, req.clinician_notes or "")
    if not success:
        raise HTTPException(status_code=404, detail="Assessment not found")
    logger.info(f"Clinician acknowledged assessment {req.assessment_id}")
    return {
        "status": "success",
        "message": f"Assessment {req.assessment_id} marked as reviewed by clinician",
        "clinician_name": req.clinician_name
    }

# Mount static frontend files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    # Mount css, js, and static folders
    css_dir = os.path.join(FRONTEND_DIR, "css")
    js_dir = os.path.join(FRONTEND_DIR, "js")
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    # Serve HTML pages directly at convenient routes
    @app.get("/", include_in_schema=False)
    @app.get("/index.html", include_in_schema=False)
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/assessment", include_in_schema=False)
    @app.get("/assessment.html", include_in_schema=False)
    def serve_assessment():
        return FileResponse(os.path.join(FRONTEND_DIR, "assessment.html"))

    @app.get("/facilities", include_in_schema=False)
    @app.get("/facilities.html", include_in_schema=False)
    def serve_facilities():
        return FileResponse(os.path.join(FRONTEND_DIR, "facilities.html"))

    @app.get("/dashboard", include_in_schema=False)
    @app.get("/dashboard.html", include_in_schema=False)
    def serve_dashboard():
        return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

    @app.get("/clinician", include_in_schema=False)
    @app.get("/clinician.html", include_in_schema=False)
    def serve_clinician():
        return FileResponse(os.path.join(FRONTEND_DIR, "clinician.html"))
