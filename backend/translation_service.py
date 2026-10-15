import re
from typing import Dict, List, Tuple, Any, Optional

SUPPORTED_LANGUAGES = [
    {
        "code": "en",
        "name": "English",
        "native": "English",
        "voice_locale": "en-IN",
        "flag": "🇬🇧"
    },
    {
        "code": "ta",
        "name": "Tamil",
        "native": "தமிழ்",
        "voice_locale": "ta-IN",
        "flag": "🇮🇳"
    },
    {
        "code": "hi",
        "name": "Hindi",
        "native": "हिन्दी",
        "voice_locale": "hi-IN",
        "flag": "🇮🇳"
    }
]

# Medical term lexicon across Tamil, Hindi, and common Roman transliterations
MEDICAL_LEXICON: Dict[str, Dict[str, Any]] = {
    # Cardiac & Severe Red Flags
    "chest pain": {
        "en": "chest pain",
        "ta": ["நெஞ்சு வலி", "நெஞ்சு பாரம்", "மார் வலி", "நெஞ்சு அடைப்பது போல்"],
        "ta_translit": ["nenju vali", "nenju param", "maar vali", "nenju erichal"],
        "hi": ["सीने में दर्द", "छाती में दर्द", "सीने में भारीपन", "सीने में जलन"],
        "hi_translit": ["seene mein dard", "seene me dard", "chhati me dard"],
        "category": "EMERGENCY_SIGN"
    },
    "difficulty breathing": {
        "en": "difficulty breathing",
        "ta": ["மூச்சுத்திணறல்", "மூச்சு திணறல்", "மூச்சு வாங்குகிறது", "மூச்சு விட முடியவில்லை"],
        "ta_translit": ["moochu thinaral", "moochu vaanguthu", "moochu vida mudiyavillai"],
        "hi": ["सांस लेने में तकलीफ", "सांस फूलना", "दम घुटना", "सांस नहीं आ रही"],
        "hi_translit": ["saans lene me takleef", "saans phoolna", "dum ghutna"],
        "category": "EMERGENCY_SIGN"
    },
    "fainting / loss of consciousness": {
        "en": "fainting / loss of consciousness",
        "ta": ["மயக்கம்", "மயங்கி விழுந்தார்", "சுயநினைவு இல்லை", "மயங்கி விழுந்து"],
        "ta_translit": ["mayakkam", "mayangi vizhundhar", "suyaninaivu illai"],
        "hi": ["बेहोशी", "बेहोश हो जाना", "चक्कर आकर गिरना", "अचेत"],
        "hi_translit": ["behosh", "behoshi", "chakkar aana", "gira"],
        "category": "EMERGENCY_SIGN"
    },
    "severe bleeding": {
        "en": "severe bleeding / hemorrhage",
        "ta": ["அதிக ரத்தப்போக்கு", "ரத்தம் நிற்கவில்லை", "ரத்த வாந்தி", "ரத்தம் கொட்டுகிறது"],
        "ta_translit": ["adhika rathapokku", "ratham nirkavillai", "ratha vaanthi"],
        "hi": ["भारी रक्तस्राव", "खून बहना", "खून की उल्टी", "रक्त बह रहा है"],
        "hi_translit": ["bhaari khoon", "khoon ki ulti", "khoon beh raha hai"],
        "category": "EMERGENCY_SIGN"
    },
      "snakebite / venomous sting": {
        "en": "snakebite / venomous bite",
        "ta": ["பாம்பு கடி", "பாம்புகடி", "தேள் கொட்டு", "விஷக்கடி"],
        "ta_translit": ["paambu kadi", "thel kottu", "visha kadi"],
        "hi": ["सांप का काटना", "सांप ने काटा", "बिच्छू का डंक", "जहरीला कीड़ा"],
        "hi_translit": ["saanp ka katna", "saanp ne kaata", "bichhoo"],
        "category": "EMERGENCY_SIGN"
    },
    "animal bite / rabies risk": {
        "en": "animal bite / dog bite (rabies risk)",
        "ta": ["நாய்க்கடி", "நாய்கடி", "வெறிநாய் கடி", "விலங்கு கடி"],
        "ta_translit": ["naai kadi", "naaikadi", "veri naai kadi"],
        "hi": ["कुत्ते का काटना", "कुत्ते ने काटा", "जानवर का काटना"],
        "hi_translit": ["kutta kata", "kutte ne kata", "jaanwar ka katna"],
        "category": "EMERGENCY_SIGN"
    },
    "obstetric emergency / pregnancy complications": {
        "en": "pregnancy complications / obstetric red flag",
        "ta": ["கர்ப்பிணி ரத்தப்போக்கு", "கர்ப்பிணி வயிற்று வலி", "கர்ப்ப காலத்தில் வலி", "கர்ப்பிணிக்கு ரத்தம்", "கர்ப்பிணி"],
        "ta_translit": ["karppini rathapokku", "karppam vali", "garbham vali"],
        "hi": ["गर्भावस्था में रक्तस्राव", "गर्भावस्था में तेज दर्द", "गर्भ में दर्द", "गर्भवती"],
        "hi_translit": ["garbhavastha me dard", "pregnancy me bleeding"],
        "category": "EMERGENCY_SIGN"
    },
    "severe burn injury": {
        "en": "severe burn injury",
        "ta": ["தீக்காயம்", "தீ காயம்", "வெந்த புண்", "தீயில் காயம்"],
        "ta_translit": ["theekayam", "thee kaayam", "ventha pun"],
        "hi": ["गंभीर जलन", "आग से जलना", "जल जाना"],
        "hi_translit": ["aag se jalna", "jal gaya", "severe burn"],
        "category": "EMERGENCY_SIGN"
    },
    "pediatric lethargy / severe dehydration": {
        "en": "pediatric lethargy / inability to feed",
        "ta": ["குழந்தை பால் குடிக்கவில்லை", "குழந்தை சோர்வு", "குழந்தைக்கு சிறுநீர் போகவில்லை"],
        "ta_translit": ["kuzhandhai paal kudikkala", "kuzhandhai sorvu"],
        "hi": ["बच्चा दूध नहीं पी रहा", "बच्चे में अत्यधिक कमजोरी", "पेशाब नहीं होना"],
        "hi_translit": ["bacha doodh nahi pee raha", "bacha behosh"],
        "category": "EMERGENCY_SIGN"
    },
    # Urgent Conditions
    "high fever": {
        "en": "high fever",
        "ta": ["கடும் காய்ச்சல்", "அதிக காய்ச்சல்", "காய்ச்சல் 4 நாட்களாக", "காய்ச்சல் 5 நாள்", "காய்ச்சல் ஒரு வாரம்", "சூடான காய்ச்சல்"],
        "ta_translit": ["kadum kaichal", "adhika kaichal", "suram", "kaichal 5 naal", "kaichal 4 naal"],
        "hi": ["तेज बुखार", "बुखार बहुत ज्यादा", "कपकपी के साथ बुखार", "बुखार 4 दिन से", "बुखार 5 दिन से"],
        "hi_translit": ["tez bukhar", "bukhar bahot jyada", "kapkapi bukhar", "5 din se bukhar", "4 din se bukhar"],
        "category": "URGENT_SIGN"
    },
    "persistent vomiting": {
        "en": "persistent vomiting / inability to keep fluids",
        "ta": ["தொடர் வாந்தி", "தண்ணீர் கூட குடிக்க முடியவில்லை", "வாந்தி நிற்கவில்லை"],
        "ta_translit": ["thodar vaanthi", "vaanthi nirkavillai", "thanni kudika mudiyala"],
        "hi": ["लगातार उल्टी", "पानी भी नहीं पच रहा", "उल्टी बंद नहीं हो रही"],
        "hi_translit": ["lagatar ulti", "pani bhi nahi ruk raha"],
        "category": "URGENT_SIGN"
    },
    "severe abdominal pain": {
        "en": "severe abdominal pain",
        "ta": ["கடுமையான வயிற்று வலி", "வயிற்றில் தாங்க முடியாத வலி", "வயிற்று வலி"],
        "ta_translit": ["kadumayana vayitru vali", "vayitru vali", "vayiru vali"],
        "hi": ["पेट में तेज दर्द", "असहनीय पेट दर्द", "पेट में मरोड़"],
        "hi_translit": ["pet me tez dard", "pet dard", "pet me marod"],
        "category": "URGENT_SIGN"
    },
    "suspected fracture / severe bone injury": {
        "en": "suspected fracture / severe bone injury",
        "ta": ["எலும்பு முறிவு", "கை உடைந்துவிட்டது", "கால் வீக்கம் நடக்க முடியவில்லை"],
        "ta_translit": ["elumbu murivu", "kai udaivathu", "nadakka mudiyala"],
        "hi": ["हड्डी टूटना", "हाथ पैर में फ्रैक्चर", "चलने में असमर्थ"],
        "hi_translit": ["haddi tootna", "fracture", "chal nahi pa raha"],
        "category": "URGENT_SIGN"
    },
    "acute eye injury / vision loss": {
        "en": "acute eye trauma / sudden vision loss",
        "ta": ["கண்ணில் காயம்", "திடீர் பார்வை இழப்பு", "கண்ணில் ரத்தம்"],
        "ta_translit": ["kannil kaayam", "paarvai theriyavillai"],
        "hi": ["आंख में गंभीर चोट", "अचानक रोशनी जाना", "आंख से खून"],
        "hi_translit": ["aankh me chot", "roshni chali gayi"],
        "category": "URGENT_SIGN"
    },
    "diabetic hypoglycemia": {
        "en": "suspected hypoglycemia / low blood sugar",
        "ta": ["சர்க்கரை குறைவு", "சர்க்கரை குறைந்து நடுக்கம்", "சுகர் லோ"],
        "ta_translit": ["sugar low", "sarkkarai kuraivu", "sugar kuraivu"],
        "hi": ["शुगर लो होना", "डायबिटीज चक्कर", "कंपकंपी और पसीना"],
        "hi_translit": ["sugar kam hona", "low sugar", "sugar girna"],
        "category": "URGENT_SIGN"
    },
    # Routine / Mild Symptoms
    "mild fever": {
        "en": "mild fever",
        "ta": ["லேசான காய்ச்சல்", "காய்ச்சல்", "சுரம்"],
        "ta_translit": ["lesana kaichal", "kaichal", "suram"],
        "hi": ["हल्का बुखार", "बुखार", "हरारत"],
        "hi_translit": ["halka bukhar", "bukhar", "hararat"],
        "category": "ROUTINE_SIGN"
    },
    "headache": {
        "en": "headache",
        "ta": ["தலைவலி", "தலை வலி", "தலை பாரம்"],
        "ta_translit": ["thalai vali", "thalaivali", "thalai param"],
        "hi": ["सिरदर्द", "सिर दर्द", "सिर में भारीपन"],
        "hi_translit": ["sirdard", "sir dard", "sar dard"],
        "category": "ROUTINE_SIGN"
    },
    "cough and cold": {
        "en": "cough and cold / running nose",
        "ta": ["இருமல்", "சளி", "மூக்கு ஒழுகுதல்", "தொண்டை வலி"],
        "ta_translit": ["irumal", "sali", "mooku ozhuguthal", "thondai vali"],
        "hi": ["खांसी", "जुकाम", "सर्दी", "नाक बहना", "गले में खराश"],
        "hi_translit": ["khansi", "jukam", "sardi", "gale me kharash"],
        "category": "ROUTINE_SIGN"
    },
    "fatigue / body pain": {
        "en": "fatigue / generalized body ache",
        "ta": ["உடல் வலி", "அசதி", "களைப்பு", "உடல் சோர்வு"],
        "ta_translit": ["udal vali", "asathi", "udambu vali", "sorvu"],
        "hi": ["बदन दर्द", "थकान", "कमजोरी", "सुस्ती"],
        "hi_translit": ["badan dard", "thakan", "kamjori"],
        "category": "ROUTINE_SIGN"
    },
    "skin rash / itching": {
        "en": "mild skin rash / itching",
        "ta": ["அரிப்பு", "தடிப்பு", "தோல் தடிப்பு"],
        "ta_translit": ["arippu", "thadippu", "thol arippu"],
        "hi": ["खुजली", "चकत्ते", "त्वचा पर दाने"],
        "hi_translit": ["khujli", "daane", "chakatte"],
        "category": "ROUTINE_SIGN"
    }
}

class MultilingualService:
    def __init__(self):
        self.lexicon = MEDICAL_LEXICON

    def extract_duration(self, text: str) -> Optional[str]:
        """Extracts duration mentioned in text in English, Tamil, or Hindi."""
        t_lower = text.lower()
        if re.search(r'\b(4|5|6|7)\s*days?\b', t_lower):
            return "4-7 days"
        if re.search(r'\b(1|2|3)\s*days?\b', t_lower):
            return "1-3 days"
        if re.search(r'\b(1|one|2|two)\s*weeks?\b', t_lower) or "> 1 week" in t_lower:
            return "> 1 week"
        if re.search(r'\b(hours?|மணிநேரம்|घंटे)\b', t_lower) or "today" in t_lower or "இன்று" in t_lower or "आज" in t_lower:
            return "< 24 hours"
        
        # Tamil patterns
        if re.search(r'(4|5|6|7)\s*(நாட்கள்|நாளா|நாள்)', text):
            return "4-7 days"
        if re.search(r'(1|2|3)\s*(நாட்கள்|நாளா|நாள்)', text):
            return "1-3 days"
        if "வாரம்" in text or "வாரமா" in text:
            return "> 1 week"
            
        # Hindi patterns
        if re.search(r'(4|5|6|7)\s*(दिन)', text):
            return "4-7 days"
        if re.search(r'(1|2|3)\s*(दिन)', text):
            return "1-3 days"
        if "हफ्ते" in text or "सप्ताह" in text:
            return "> 1 week"
            
        return None

    def detect_language(self, text: str) -> str:
        """Determines if text is primarily Tamil, Hindi, or English (Script & Latin)."""
        tamil_range = range(0x0B80, 0x0BFF + 1)
        hindi_range = range(0x0900, 0x097F + 1)
        
        ta_count = sum(1 for ch in text if ord(ch) in tamil_range)
        hi_count = sum(1 for ch in text if ord(ch) in hindi_range)
        
        if ta_count > 1:
            return "ta"
        if hi_count > 1:
            return "hi"
            
        # Check transliterated markers
        text_lower = text.lower()
        for term, data in self.lexicon.items():
            for t_phr in data.get("ta_translit", []):
                if t_phr in text_lower:
                    return "ta"
            for h_phr in data.get("hi_translit", []):
                if h_phr in text_lower:
                    return "hi"
                    
        return "en"

    def translate_and_normalize(self, text: str, source_lang: str = "auto") -> Tuple[str, List[str], str]:
        """
        Translates and maps multi-lingual symptom descriptions into standardized
        clinical English phrases, extracting detected clinical concepts.
        Returns (normalized_english_text, detected_terms, identified_lang).
        """
        if source_lang == "auto" or not source_lang:
            identified_lang = self.detect_language(text)
        else:
            identified_lang = source_lang

        detected_terms = []
        translated_segments = []
        text_lower = text.lower()

        # Match against our comprehensive medical lexicon
        for std_term, term_data in self.lexicon.items():
            matched = False
            
            # Check English
            if std_term in text_lower:
                matched = True
            
            # Check Tamil Native Script
            if not matched:
                for ta_w in term_data.get("ta", []):
                    if ta_w.lower() in text_lower or ta_w in text:
                        matched = True
                        break
            
            # Check Tamil Transliteration
            if not matched:
                for ta_tr in term_data.get("ta_translit", []):
                    if re.search(r'\b' + re.escape(ta_tr) + r'\b', text_lower):
                        matched = True
                        break

            # Check Hindi Native Script
            if not matched:
                for hi_w in term_data.get("hi", []):
                    if hi_w.lower() in text_lower or hi_w in text:
                        matched = True
                        break

            # Check Hindi Transliteration
            if not matched:
                for hi_tr in term_data.get("hi_translit", []):
                    if re.search(r'\b' + re.escape(hi_tr) + r'\b', text_lower):
                        matched = True
                        break

            if matched:
                detected_terms.append(std_term)
                translated_segments.append(term_data["en"])

        if identified_lang == "en":
            normalized_text = text
            if translated_segments:
                normalized_text = f"{text} (Key clinical concepts: {', '.join(detected_terms)})"
        else:
            if translated_segments:
                normalized_text = f"Reported: '{text}'. Translated Clinical Findings: {', '.join(translated_segments)}."
            else:
                normalized_text = f"Reported in {identified_lang.upper()}: '{text}'."

        return normalized_text, detected_terms, identified_lang

translation_service = MultilingualService()
