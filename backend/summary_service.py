import uuid
from datetime import datetime
from typing import List, Dict, Any
from .schemas import MedicalSummaryRequest, MedicalSummaryResponse

def generate_medical_summary(req: MedicalSummaryRequest) -> MedicalSummaryResponse:
    summary_id = f"SUM-{uuid.uuid4().hex[:8].upper()}"
    generated_at = datetime.utcnow().strftime("%d %b %Y, %I:%M %p UTC")

    # Detect pertinent negatives / important missing information
    missing_info: List[str] = []
    
    if not req.duration or req.duration.strip() == "":
        missing_info.append("Exact onset time / duration of symptoms not specified by patient.")
    
    context_lower = (req.additional_context or "").lower()
    combined_symptoms = f"{req.symptoms_text} {req.translated_text or ''}".lower()
    
    if not any(k in context_lower for k in ["diabet", "bp", "hyper", "asthma", "heart", "pregnant", "none"]):
        missing_info.append("Pre-existing chronic medical history (Diabetes, Hypertension, Cardiac, Pregnancy) unconfirmed.")
        
    if "allergy" not in context_lower and "allergic" not in context_lower:
        missing_info.append("Known drug allergies not documented.")

    # Fever & Vital checks (multilingual: English, Tamil, Hindi)
    fever_markers = ["fever", "காய்ச்சல்", "சுரம்", "புஹார்", "बुखार", "kaichal", "bukhar"]
    temp_markers = ["temp", "thermometer", "degree", "பாரன்ஹீட்", "டிகிரி", "तापमान", "fever reading"]
    if any(fm in combined_symptoms for fm in fever_markers) and not any(tm in combined_symptoms for tm in temp_markers):
        missing_info.append("Numerical body temperature (thermometer reading in °F / °C) not recorded.")

    # Cardiac domain pertinent negatives
    cardio_markers = ["chest pain", "heart", "pressure on chest", "நெஞ்சு", "सीने में"]
    if any(cm in combined_symptoms for cm in cardio_markers):
        missing_info.append("Baseline blood pressure and emergency 12-lead ECG not documented.")
        missing_info.append("History of prior myocardial infarction, angina, or stent placement unverified.")

    # Respiratory domain pertinent negatives
    resp_markers = ["breathing", "breathlessness", "asthma", "மூச்சு", "सांस"]
    if any(rm in combined_symptoms for rm in resp_markers):
        missing_info.append("Peripheral pulse oximetry (SpO2 oxygen saturation percentage) not recorded.")

    # Pediatric domain pertinent negatives
    if (req.age_group or "").lower() == "child":
        missing_info.append("Child immunization card / vaccination schedule compliance unverified.")
        missing_info.append("Oral hydration tolerance and recent urination / wet diaper frequency unrecorded.")

    # Animal bite pertinent negatives
    bite_markers = ["dog bite", "animal bite", "rabies", "நாய்க்கடி", "நாய்கடி", "कुत्ते"]
    if any(bm in combined_symptoms for bm in bite_markers):
        missing_info.append("Immediate 15-minute soap and water wound lavage status unverified.")
        missing_info.append("Biting animal rabies observation / vaccination status unknown.")

    # Chief complaint preservation
    original_snippet = req.symptoms_text.strip()
    if req.language != "en" and req.translated_text:
        chief_complaint = f"Original [{req.language.upper()}]: \"{original_snippet}\"\nClinical Translation: \"{req.translated_text}\""
    else:
        chief_complaint = f"\"{original_snippet}\""

    # Rich clinical rationale explanation
    red_flag_str = f" Red Flags: {', '.join(req.red_flags_detected)}." if req.red_flags_detected else ""
    rationale = f"Evaluated under MedPulse AI Clinical Triage Protocol. Urgency Category: {req.urgency_category}.{red_flag_str} Recommended Level of Care: {req.recommended_facility_type}. Action: {req.recommended_action}"

    return MedicalSummaryResponse(
        summary_id=summary_id,
        generated_at=generated_at,
        chief_complaint=chief_complaint,
        reported_language=req.language.upper(),
        duration=req.duration if req.duration else "Unspecified duration",
        age_group=req.age_group.capitalize() if req.age_group else "Adult",
        recognized_symptoms=req.recognized_symptoms if req.recognized_symptoms else ["General symptoms reported"],
        pertinent_negatives=missing_info,
        urgency_assessment=req.urgency_category,
        clinical_rationale=rationale,
        recommended_level_of_care=req.recommended_facility_type,
        is_editable_draft=True,
        disclaimer="Draft generated for clinical review. Must be validated by an attending healthcare professional."
    )
