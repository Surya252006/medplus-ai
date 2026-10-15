from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LanguageOption(BaseModel):
    code: str
    name: str
    native: str
    voice_locale: str
    flag: str

class TriageRequest(BaseModel):
    symptoms_text: str = Field(..., min_length=2, max_length=2000, description="Description of symptoms")
    language: str = Field(default="en", description="Language code: en, ta, hi")
    age_group: Optional[str] = Field(default="adult", description="child, teen, adult, senior")
    duration: Optional[str] = Field(default="", description="e.g., < 24 hours, 1-3 days, 1 week, > 1 month")
    additional_context: Optional[str] = Field(default="", description="Existing conditions or context")
    vital_signs: Optional[Dict[str, Any]] = Field(default=None, description="Optional pulse, temp, bp")
    save_to_history: Optional[bool] = Field(default=False, description="User consent to save to history")

class TriageResponse(BaseModel):
    urgency_category: str = Field(..., description="EMERGENCY, URGENT, ROUTINE")
    urgency_color: str = Field(..., description="Hex color: #EF4444, #F59E0B, #10B981")
    urgency_title: str = Field(..., description="High-level category label")
    explanation: str = Field(..., description="Clear explanation of urgency level")
    recognized_symptoms: List[str] = Field(default_factory=list, description="Recognized clinical symptoms")
    red_flags_detected: List[str] = Field(default_factory=list, description="Red flag warning signs found")
    recommended_action: str = Field(..., description="Actionable next steps")
    recommended_facility_type: str = Field(..., description="Recommended facility level (e.g. Hospital, CHC, PHC)")
    safety_warnings: List[str] = Field(default_factory=list, description="Crucial safety warnings and emergency numbers")
    clinical_rationale: str = Field(..., description="Transparent rules triggered")
    confidence_score: float = Field(..., description="Confidence score from 0.0 to 1.0")
    disclaimer: str = Field(..., description="Clinical safety disclaimer")
    translated_symptoms: Optional[str] = Field(default="", description="Normalized English translation if input was in Tamil or Hindi")
    assessment_id: Optional[str] = Field(default=None, description="ID if saved to history")
    localized_urgency_title: Optional[str] = Field(default="", description="Localized title in patient language")
    localized_explanation: Optional[str] = Field(default="", description="Localized explanation in patient language")
    localized_action: Optional[str] = Field(default="", description="Localized action in patient language")
    localized_warnings: Optional[List[str]] = Field(default_factory=list, description="Localized safety warnings")

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    source_lang: str = Field(default="auto")
    target_lang: str = Field(default="en")

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float
    detected_terms: List[str] = Field(default_factory=list)

class MedicalSummaryRequest(BaseModel):
    symptoms_text: str
    translated_text: Optional[str] = ""
    language: str = "en"
    age_group: Optional[str] = "adult"
    duration: Optional[str] = ""
    additional_context: Optional[str] = ""
    urgency_category: str
    recognized_symptoms: List[str] = Field(default_factory=list)
    red_flags_detected: List[str] = Field(default_factory=list)
    recommended_action: str
    recommended_facility_type: str

class MedicalSummaryResponse(BaseModel):
    summary_id: str
    generated_at: str
    chief_complaint: str
    reported_language: str
    duration: str
    age_group: str
    recognized_symptoms: List[str]
    pertinent_negatives: List[str]
    urgency_assessment: str
    clinical_rationale: str
    recommended_level_of_care: str
    is_editable_draft: bool = True
    disclaimer: str

class FacilityItem(BaseModel):
    id: str
    name: str
    type: str
    category: str
    address: str
    village_town: str
    district: str
    pincode: str
    latitude: float
    longitude: float
    phone: str
    emergency_phone: str
    is_24x7_emergency: bool
    services: List[str]
    doctor_availability: str
    transport_info: str
    is_demo_data: bool
    verified_label: str
    distance_km: Optional[float] = None

class FacilityListResponse(BaseModel):
    total: int
    facilities: List[FacilityItem]
    query_used: Optional[str] = None
    applied_category: Optional[str] = None
    user_location: Optional[Dict[str, float]] = None

class SavedAssessment(BaseModel):
    id: str
    created_at: str
    symptoms_original: str
    language: str
    age_group: str
    duration: str
    urgency_category: str
    urgency_color: str
    recommended_facility_type: str
    summary_text: str
    clinician_acknowledged: bool = False
    clinician_notes: Optional[str] = ""

class ClinicianAcknowledgeRequest(BaseModel):
    assessment_id: str
    clinician_name: str = "Dr. On-Duty / ASHA Supervisor"
    clinician_notes: Optional[str] = ""
