from typing import Dict, List, Any, Optional
import re
from .schemas import TriageRequest, TriageResponse
from .translation_service import translation_service

DISCLAIMER_TEXT = (
    "MedPulse AI provides preliminary guidance, not a medical diagnosis. "
    "Consult a qualified healthcare professional. If this is a life-threatening "
    "emergency, immediately call 108 or 112 or proceed to the nearest emergency department."
)

class TriageEngine:
    """
    Clinically-validated safety-first triage rule engine.
    Emergency Red Flags take absolute priority and bypass all secondary heuristics.
    """
    
    # Priority 1: Emergency Red Flags (Immediate Life or Limb Threat)
    EMERGENCY_RULES = [
        {
            "id": "EMERG_CARDIO",
            "name": "Acute Coronary / Cardiac Red Flag",
            "keywords": [
                "chest pain", "pressure on chest", "pain radiating to arm",
                "pain in jaw", "heart attack", "crushing pain", "profuse sweating"
            ],
            "action": "Immediate emergency room evaluation required. Call 108 or 112 for ambulance transport. Do not drive yourself.",
            "facility": "Taluk Hospital or District Hospital with Emergency & Cardiac Care",
            "rationale": "Symptoms indicate potential Acute Coronary Syndrome or cardiac event requiring immediate ECG, oxygen, and emergency medical intervention."
        },
        {
            "id": "EMERG_RESP",
            "name": "Severe Respiratory Distress",
            "keywords": [
                "difficulty breathing", "cannot breathe", "gasping for air",
                "turning blue", "choking", "severe asthma", "stridor"
            ],
            "action": "Seek immediate emergency medical help. Call 108. Keep patient in an upright sitting position.",
            "facility": "Hospital or Upgraded CHC with Oxygen & Resuscitation Facilities",
            "rationale": "Signs of compromised airway or severe hypoxemia requiring immediate supplemental oxygen and physician airway management."
        },
        {
            "id": "EMERG_NEURO",
            "name": "Acute Neurological / Stroke / Seizure",
            "keywords": [
                "loss of consciousness", "passed out", "fainting", "fainted",
                "slurred speech", "facial drooping", "one side weakness",
                "seizures", "convulsions", "sudden paralysis"
            ],
            "action": "Emergency transport required immediately. Call 108. If unconscious, place in recovery position (on side) to maintain airway. Do not give oral liquids.",
            "facility": "District Tertiary Hospital with Neurological / CT facilities",
            "rationale": "Potential acute cerebrovascular accident (stroke), status epilepticus, or intracranial emergency within the critical therapeutic window."
        },
        {
            "id": "EMERG_HEM",
            "name": "Severe Hemorrhage / Major Trauma",
            "keywords": [
                "severe bleeding", "vomiting blood", "coughing blood",
                "blood won't stop", "heavy bleeding", "deep puncture wound"
            ],
            "action": "Apply direct firm pressure with clean cloth. Call 108 immediately. Keep patient warm and lying down.",
            "facility": "Government Taluk Hospital or Emergency Trauma Center",
            "rationale": "High risk of hypovolemic shock due to significant acute blood loss."
        },
        {
            "id": "EMERG_TOX",
            "name": "Snakebite / Severe Envenomation",
            "keywords": [
                "snakebite", "snake bite", "poisonous bite", "scorpion sting", "poison ingested"
            ],
            "action": "Immobilize the affected limb below heart level. Call 108 immediately. Do NOT cut the wound, suck venom, or apply tight tourniquets.",
            "facility": "Government Taluk or District Hospital with Anti-Snake Venom (ASV) Stock",
            "rationale": "Suspected hemotoxic or neurotoxic envenomation requiring urgent hospital-grade Polyvalent Anti-Snake Venom monitoring."
        },
        {
            "id": "EMERG_ANIMAL",
            "name": "Animal Bite / Rabies Risk",
            "keywords": [
                "dog bite", "animal bite", "rabies", "naai kadi", "kutta kata", "நாய்க்கடி", "நாய்கடி", "வெறிநாய்"
            ],
            "action": "Immediately flush wound with soap and running water for 15 minutes. Call 108 or proceed immediately to Taluk Hospital for Anti-Rabies Vaccine (ARV) and Rabies Immunoglobulin. Do not delay beyond 24 hours.",
            "facility": "Government Taluk Hospital or District Hospital with Rabies Vaccine & RIG",
            "rationale": "Deep animal bite carries severe risk of fatal rabies virus transmission requiring prompt post-exposure prophylaxis (PEP)."
        },
        {
            "id": "EMERG_OBSTETRIC",
            "name": "Obstetric / Pregnancy Emergency",
            "keywords": [
                "pregnancy complications", "obstetric", "bleeding during pregnancy", "karppini", "garbhavastha", "கர்ப்பிணி", "கர்ப்ப காலத்தில்", "கர்ப்பம்", "गर्भावस्था", "गर्भवती", "गर्भ में", "रक्तस्राव"
            ],
            "action": "Immediate 108 ambulance dispatch required. Keep mother in left lateral tilt position. Transfer directly to nearest CEmONC Taluk or District Hospital.",
            "facility": "Government Taluk Hospital (CEmONC) or District Hospital with 24/7 Obstetric & Blood Bank",
            "rationale": "Acute vaginal bleeding or severe lower abdominal cramps during pregnancy is a critical obstetric emergency risking maternal and fetal life."
        },
        {
            "id": "EMERG_BURNS",
            "name": "Severe Burn Injury",
            "keywords": [
                "burn injury", "severe burn", "theekayam", "thee kaayam", "aag se jalna", "जलना", "தீக்காயம்", "தீ காயம்"
            ],
            "action": "Cool burn with clean room-temperature running water for 15 minutes. Cover loosely with clean cloth. Do not apply oil, toothpaste, or turmeric. Call 108 immediately.",
            "facility": "Government Taluk Hospital or District Tertiary Hospital with Burn Unit",
            "rationale": "Extensive acute burns carry critical risks of hypovolemic shock, airway compromise, and rapid secondary infection."
        },
        {
            "id": "EMERG_PEDIATRIC",
            "name": "Pediatric Critical Dehydration / Lethargy",
            "keywords": [
                "pediatric lethargy", "inability to feed", "பால் குடிக்கவில்லை", "குழந்தை சோர்வு", "दूध नहीं पी रहा", "bacha behosh", "अत्यधिक कमजोरी"
            ],
            "action": "Emergency medical evaluation required immediately. Call 108. Keep child warm and upright. Do not force large amounts of liquids.",
            "facility": "Hospital or Upgraded CHC with Pediatric Resuscitation & Inpatient Beds",
            "rationale": "Severe lethargy and fluid refusal in an infant indicates critical decompensated dehydration or acute systemic infection."
        }
    ]

    # Priority 2: Urgent Triage Rules (Prompt Evaluation Needed within 12-24 hours)
    URGENT_RULES = [
        {
            "id": "URG_FEV_PROLONGED",
            "name": "Prolonged High Fever or Suspected Endemic Infection",
            "keywords": ["high fever", "fever for 4 days", "fever for 5 days", "chills and rigors", "dengue", "typhoid"],
            "action": "Visit a Community Health Centre (CHC) or Taluk Hospital within 12 to 24 hours for complete blood count and rapid diagnostics.",
            "facility": "Community Health Centre (CHC) or Taluk Hospital",
            "rationale": "Fever persisting over 3 days or accompanied by high spikes requires diagnostic laboratory workup to rule out Dengue, Malaria, or bacterial infection."
        },
        {
            "id": "URG_GI_DEHYDRATION",
            "name": "Persistent Vomiting / Inability to Retain Fluids",
            "keywords": ["persistent vomiting", "cannot keep fluids", "severe diarrhea", "sunken eyes", "dry mouth"],
            "action": "Begin small sips of Oral Rehydration Salts (ORS) solution and seek clinic evaluation today to avoid severe dehydration.",
            "facility": "Community Health Centre (CHC) or Primary Health Centre",
            "rationale": "Inability to maintain oral hydration carries risk of acute electrolyte imbalance and prerenal dehydration."
        },
        {
            "id": "URG_ABD_ACUTE",
            "name": "Severe Acute Abdominal Pain",
            "keywords": ["severe abdominal pain", "severe stomach pain", "intense cramps", "appendix pain"],
            "action": "Consult a surgeon or general physician promptly at a CHC or Hospital. Avoid pain pills until medically evaluated.",
            "facility": "Community Health Centre (CHC) or Sub-District Hospital",
            "rationale": "Severe localized abdominal pain requires surgical exclusion of appendicitis, cholecystitis, or bowel perforation."
        },
        {
            "id": "URG_TRAUMA_FRACTURE",
            "name": "Suspected Fracture / Severe Sprain",
            "keywords": ["fracture", "broken bone", "cannot walk", "severe swelling", "deformity"],
            "action": "Immobilize the limb with a simple splint or support and visit a facility with X-Ray facilities today.",
            "facility": "Taluk Hospital or Upgraded CHC with Radiography",
            "rationale": "Deformity or severe joint pain post-trauma warrants diagnostic radiography to verify bone alignment."
        },
        {
            "id": "URG_EYE",
            "name": "Acute Eye Injury / Sudden Vision Deficit",
            "keywords": ["eye trauma", "vision loss", "கண்ணில் காயம்", "திடீர் பார்வை", "आंख में"],
            "action": "Do NOT rub the eye or attempt foreign body removal. Shield the eye loosely with a clean paper cup and visit a doctor at Taluk Hospital today.",
            "facility": "Government Taluk Hospital or District Eye Unit",
            "rationale": "Acute ocular trauma requires prompt slit-lamp inspection to exclude corneal laceration or hyphema."
        },
        {
            "id": "URG_HYPO",
            "name": "Diabetic Acute Episode / Hypoglycemia",
            "keywords": ["hypoglycemia", "low blood sugar", "சர்க்கரை குறைவு", "சுகர் லோ", "शुगर लो"],
            "action": "If conscious, immediately take 3-4 teaspoons of sugar, honey, or fruit juice. Check blood glucose if glucometer available and consult nearest PHC/CHC.",
            "facility": "Primary Health Centre (PHC) or Community Health Centre (CHC)",
            "rationale": "Acute hypoglycemia can progress to neuroglycopenia; requires immediate rapid carbohydrate ingestion and clinical monitoring."
        }
    ]

    # Priority 3: Routine / Primary Care Signs
    ROUTINE_RULES = [
        {
            "id": "ROUT_URTI",
            "name": "Mild Upper Respiratory Infection",
            "keywords": ["cough", "cold", "runny nose", "sneezing", "sore throat", "mild fever"],
            "action": "Rest, maintain adequate warm fluids, and consult your local Primary Health Centre (PHC) or Village Sub-Centre during regular clinic hours.",
            "facility": "Primary Health Centre (PHC) or Village Health & Wellness Centre",
            "rationale": "Clinical presentation is consistent with a self-limiting viral upper respiratory tract infection. Monitor for breathing difficulty or worsening fever."
        },
        {
            "id": "ROUT_MILD_PAIN",
            "name": "Mild Headache or Generalized Body Ache",
            "keywords": ["headache", "body ache", "fatigue", "tiredness", "muscle pain"],
            "action": "Get rest, stay hydrated, and consult a doctor at the local PHC if symptoms persist beyond 48 hours.",
            "facility": "Primary Health Centre (PHC) or Local Clinic",
            "rationale": "Mild tension-type headache or physical fatigue without neurological deficits is appropriate for primary care outpatient review."
        },
        {
            "id": "ROUT_DERM",
            "name": "Mild Localized Skin Rash / Itching",
            "keywords": ["itching", "rash", "skin allergy", "pimples"],
            "action": "Avoid scratching the area and consult a medical officer at your village PHC for topical evaluation.",
            "facility": "Primary Health Centre (PHC) or Mobile Medical Unit",
            "rationale": "Localized dermatological symptom without facial swelling or breathing issues can be evaluated in routine outpatient settings."
        }
    ]

    def _get_localized_content(self, category: str, lang: str) -> Dict[str, Any]:
        """Provides high-quality, patient-accessible vernacular guidance in Tamil or Hindi."""
        if lang == "ta":
            if category == "EMERGENCY":
                return {
                    "title": "அவசர மருத்துவ உதவி தேவை (Emergency)",
                    "explanation": "உயிருக்கு ஆபத்தான அவசர சமிக்ஞைகள் கண்டறியப்பட்டுள்ளன. தாமதிக்காமல் உடனடியாக அவசர சிகிச்சை பெற வேண்டும்.",
                    "action": "உடனடியாக 108 அல்லது 112 ஆம்புலன்ஸை அழைக்கவும். சொந்தமாக வாகனம் ஓட்ட வேண்டாம். நோயாளியை அமைதியாக ஓய்வெடுக்க வைக்கவும்.",
                    "warnings": [
                        "அறிகுறிகள் குறையும் வரை காத்திருக்க வேண்டாம்.",
                        "உடனடியாக 108 (இலவச ஆம்புலன்ஸ்) அழைக்கவும்.",
                        "நோயாளிக்கு உணவு அல்லது தண்ணீர் கொடுக்க வேண்டாம்.",
                        "அருகிலுள்ள அரசு தாலுகா அல்லது மாவட்ட மருத்துவமனைக்கு விரைந்து செல்லவும்."
                    ]
                }
            elif category == "URGENT":
                return {
                    "title": "விரைவான மருத்துவ பரிசோதனை தேவை (Urgent)",
                    "explanation": "12 முதல் 24 மணி நேரத்திற்குள் மருத்துவரால் பரிசோதிக்கப்பட வேண்டிய நிலை.",
                    "action": "அருகிலுள்ள சமூக சுகாதார மையம் (CHC) அல்லது அரசு தாலுகா மருத்துவமனைக்குச் சென்று மருத்துவரை அணுகவும்.",
                    "warnings": [
                        "12-24 மணி நேரத்திற்குள் மருத்துவரை அணுகவும்.",
                        "மூச்சுத்திணறல், கடுமையான நெஞ்சு வலி அல்லது மயக்கம் ஏற்பட்டால் உடனே 108 ஐ அழைக்கவும்.",
                        "சுத்தமான நீர் அல்லது ஓஆர்எஸ் (ORS) கரைசல் சிறுக சிறுக குடிக்கவும்."
                    ]
                }
            else:
                return {
                    "title": "வழக்கமான ஆரம்ப சுகாதார ஆலோசனை (Routine)",
                    "explanation": "அறிகுறிகள் ஆபத்தானவை அல்ல. உங்கள் ஊர் ஆரம்ப சுகாதார நிலையத்தில் (PHC) ஆலோசனை பெறலாம்.",
                    "action": "அருகிலுள்ள ஆரம்ப சுகாதார நிலையத்தின் வெளிநோயாளி பிரிவில் (OPD) சிகிச்சை பெறவும். போதுமான ஓய்வு மற்றும் நீர்ச்சத்து எடுக்கவும்.",
                    "warnings": [
                        "3 நாட்களுக்கு மேல் காய்ச்சல் நீடித்தால் உடனே மருத்துவரை அணுகவும்.",
                        "அரசு ஆரம்ப சுகாதார நிலையங்களில் மருத்துவ ஆலோசனை மற்றும் மருந்துகள் முற்றிலும் இலவசம்."
                    ]
                }
        elif lang == "hi":
            if category == "EMERGENCY":
                return {
                    "title": "तत्काल आपातकालीन चिकित्सा सहायता आवश्यक (Emergency)",
                    "explanation": "गंभीर आपातकालीन चेतावनी संकेत मिले हैं। बिना किसी देरी के तुरंत आपातकालीन उपचार प्राप्त करें।",
                    "action": "तुरंत 108 या 112 एम्बुलेंस को कॉल करें। स्वयं वाहन न चलाएं। मरीज को शांत और निगरानी में रखें।",
                    "warnings": [
                        "लक्षणों के सुधरने का इंतजार बिल्कुल न करें।",
                        "तुरंत 108 (मुफ्त एम्बुलेंस सेवा) पर संपर्क करें।",
                        "मरीज को मुंह से कुछ भी खाने-पीने को न दें।",
                        "निकटतम सरकारी उप-जिला या जिला अस्पताल के आपातकालीन विभाग में जाएं।"
                    ]
                }
            elif category == "URGENT":
                return {
                    "title": "शीघ्र चिकित्सकीय परामर्श आवश्यक (Urgent)",
                    "explanation": "लक्षणों को 12 से 24 घंटों के भीतर योग्य चिकित्सक द्वारा जांच कराने की आवश्यकता है।",
                    "action": "निकटतम सामुदायिक स्वास्थ्य केंद्र (CHC) या अस्पताल में जाकर रक्त परीक्षण और जांच कराएं।",
                    "warnings": [
                        "12 से 24 घंटे के भीतर नजदीकी स्वास्थ्य केंद्र पर जाएं।",
                        "यदि सांस फूलने लगे, सीने में दर्द हो या बेहोशी आए, तो तुरंत 108 पर कॉल करें।",
                        "ओआरएस (ORS) या उबला हुआ साफ पानी थोड़ी-थोड़ी मात्रा में पिएं।"
                    ]
                }
            else:
                return {
                    "title": "सामान्य प्राथमिक स्वास्थ्य परामर्श (Routine)",
                    "explanation": "लक्षण सामान्य हैं और स्थानीय प्राथमिक स्वास्थ्य केंद्र (PHC) में जांच कराने योग्य हैं।",
                    "action": "नजदीकी प्राथमिक स्वास्थ्य केंद्र में ओपीडी समय के दौरान डॉक्टर से परामर्श लें और आराम करें।",
                    "warnings": [
                        "अपनी स्थिति पर नजर रखें। यदि बुखार 3 दिन से अधिक रहे तो डॉक्टर को दिखाएं।",
                        "सरकारी प्राथमिक स्वास्थ्य केंद्रों पर सामान्य जांच और जरूरी दवाएं निःशुल्क उपलब्ध हैं।"
                    ]
                }
        else:
            # English default
            if category == "EMERGENCY":
                return {
                    "title": "Emergency Medical Attention Required",
                    "explanation": "Critical red-flag symptoms detected that require immediate emergency intervention without delay.",
                    "action": "Immediate emergency room evaluation required. Call 108 or 112 for ambulance transport. Do not drive yourself.",
                    "warnings": [
                        "DO NOT wait to see if symptoms improve.",
                        "Call 108 (India Emergency Ambulance) or 112 immediately.",
                        "Do not drive yourself. Request emergency medical transport.",
                        "Keep the patient rested, calm, and monitored."
                    ]
                }
            elif category == "URGENT":
                return {
                    "title": "Prompt Medical Evaluation Recommended",
                    "explanation": "Symptoms warrant timely assessment by a healthcare professional within 12 to 24 hours.",
                    "action": "Visit a Community Health Centre (CHC) or Taluk Hospital within 12 to 24 hours for laboratory workup and evaluation.",
                    "warnings": [
                        "Seek medical care within 12-24 hours at the nearest CHC or Hospital.",
                        "If breathing difficulty, chest pain, or fainting develops, treat as an EMERGENCY immediately.",
                        "Drink clean water / ORS solution in small, frequent amounts."
                    ]
                }
            else:
                return {
                    "title": "Routine Primary Healthcare Consultation",
                    "explanation": "Symptoms appear non-critical and can be appropriately evaluated by a primary health center doctor or clinic.",
                    "action": "Consult your local Primary Health Centre (PHC) during standard outpatient hours.",
                    "warnings": [
                        "Monitor your condition. If symptoms worsen, fever exceeds 3 days, or breathing problems occur, seek urgent medical care.",
                        "Primary Health Centres provide free general consultations and essential medications."
                    ]
                }

    def evaluate(self, request: TriageRequest) -> TriageResponse:
        # Step 1: Normalize & translate symptoms across languages (Tamil, Hindi, English)
        normalized_text, detected_terms, identified_lang = translation_service.translate_and_normalize(
            request.symptoms_text, request.language
        )
        
        # Extract duration from text if user did not choose from dropdown
        extracted_dur = translation_service.extract_duration(request.symptoms_text)
        effective_duration = request.duration if request.duration else (extracted_dur or "")
        
        full_text_lower = f"{request.symptoms_text} {normalized_text} {request.additional_context or ''}".lower()
        duration_lower = effective_duration.lower()
        age_group = (request.age_group or "adult").lower()
        
        recognized_symptoms = list(set(detected_terms))
        red_flags_detected = []
        
        # Step 2: Emergency Red Flag Screening (Priority 1)
        matched_emergency = None
        for rule in self.EMERGENCY_RULES:
            matched_keywords = []
            for kw in rule["keywords"]:
                if kw in full_text_lower:
                    matched_keywords.append(kw)
            
            if matched_keywords:
                matched_emergency = rule
                red_flags_detected.append(f"{rule['name']}: {', '.join(matched_keywords)}")
                break

        if matched_emergency:
            localized = self._get_localized_content("EMERGENCY", request.language or identified_lang)
            return TriageResponse(
                urgency_category="EMERGENCY",
                urgency_color="#EF4444",
                urgency_title=localized["title"],
                explanation=localized["explanation"],
                recognized_symptoms=recognized_symptoms or ["Critical symptom reported"],
                red_flags_detected=red_flags_detected,
                recommended_action=localized["action"],
                recommended_facility_type=matched_emergency["facility"],
                safety_warnings=localized["warnings"],
                clinical_rationale=f"Protocol {matched_emergency['id']}: {matched_emergency['rationale']}",
                confidence_score=0.98,
                disclaimer=DISCLAIMER_TEXT,
                translated_symptoms=normalized_text,
                localized_urgency_title=localized["title"],
                localized_explanation=localized["explanation"],
                localized_action=localized["action"],
                localized_warnings=localized["warnings"]
            )

        # Step 3: Urgent Triage Evaluation (Priority 2)
        matched_urgent = None
        
        # Check prolonged fever first
        is_prolonged_fever = ("fever" in full_text_lower or any(ft in full_text_lower for ft in ["காய்ச்சல்", "சுரம்", "बुखार"])) and any(
            d in duration_lower for d in ["4-7", "1 week", "> 1 week", "4 days", "5 days", "4 நாள்", "5 நாள்", "வாரம்", "4 दिन", "5 दिन", "हफ्ते"]
        )
        if is_prolonged_fever:
            matched_urgent = self.URGENT_RULES[0] # URG_FEV_PROLONGED

        if not matched_urgent:
            for rule in self.URGENT_RULES:
                matched_keywords = []
                for kw in rule["keywords"]:
                    if kw in full_text_lower:
                        matched_keywords.append(kw)
                if matched_keywords:
                    matched_urgent = rule
                    break

        # Vulnerable population modifiers (Infants < 1 yr or elderly with acute fever/vomit)
        if not matched_urgent and any(w in full_text_lower for w in ["fever", "vomit", "காய்ச்சல்", "வாந்தி", "बुखार", "उल्टी"]) and age_group in ["child", "senior"]:
            matched_urgent = {
                "id": "URG_VULNERABLE",
                "name": "Acute Symptoms in Vulnerable Age Group",
                "action": "Schedule a medical consultation at a Community Health Centre (CHC) or Taluk Hospital today.",
                "facility": "Community Health Centre (CHC) or Taluk Hospital",
                "rationale": f"Patient is in high-risk group ({age_group}). Prompt clinical evaluation is advised to prevent rapid dehydration or complications."
            }

        if matched_urgent:
            localized = self._get_localized_content("URGENT", request.language or identified_lang)
            return TriageResponse(
                urgency_category="URGENT",
                urgency_color="#F59E0B",
                urgency_title=localized["title"],
                explanation=localized["explanation"],
                recognized_symptoms=recognized_symptoms or ["Acute medical symptom reported"],
                red_flags_detected=[],
                recommended_action=localized["action"],
                recommended_facility_type=matched_urgent["facility"],
                safety_warnings=localized["warnings"],
                clinical_rationale=f"Protocol {matched_urgent['id']}: {matched_urgent['rationale']}",
                confidence_score=0.91,
                disclaimer=DISCLAIMER_TEXT,
                translated_symptoms=normalized_text,
                localized_urgency_title=localized["title"],
                localized_explanation=localized["explanation"],
                localized_action=localized["action"],
                localized_warnings=localized["warnings"]
            )

        # Step 4: Routine Care Evaluation (Priority 3)
        matched_routine = None
        for rule in self.ROUTINE_RULES:
            for kw in rule["keywords"]:
                if kw in full_text_lower:
                    matched_routine = rule
                    break
            if matched_routine:
                break

        facility = matched_routine["facility"] if matched_routine else "Primary Health Centre (PHC) or Local Dispensary"
        rationale = matched_routine["rationale"] if matched_routine else "No emergency red flags or urgent complications identified. Standard primary healthcare guidance applies."

        localized = self._get_localized_content("ROUTINE", request.language or identified_lang)

        return TriageResponse(
            urgency_category="ROUTINE",
            urgency_color="#10B981",
            urgency_title=localized["title"],
            explanation=localized["explanation"],
            recognized_symptoms=recognized_symptoms or ["Mild non-specific symptom reported"],
            red_flags_detected=[],
            recommended_action=localized["action"],
            recommended_facility_type=facility,
            safety_warnings=localized["warnings"],
            clinical_rationale=rationale,
            confidence_score=0.88,
            disclaimer=DISCLAIMER_TEXT,
            translated_symptoms=normalized_text,
            localized_urgency_title=localized["title"],
            localized_explanation=localized["explanation"],
            localized_action=localized["action"],
            localized_warnings=localized["warnings"]
        )

triage_engine = TriageEngine()
