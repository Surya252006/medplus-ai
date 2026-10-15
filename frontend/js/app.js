// MedPulse AI — Core Application Logic & Comprehensive Client-side i18n

const I18N_DICTIONARY = {
  en: {
    // Navigation
    nav_home: "Home",
    nav_symptoms: "Check Symptoms",
    nav_facilities: "Find Healthcare",
    nav_dashboard: "My Dashboard",
    nav_clinician: "Clinician Portal",
    emergency_call_text: "Emergency? Call 108 / 112 immediately",
    
    // Landing Page
    hero_pill: "Rural & Semi-Urban Healthcare Navigation",
    hero_title: "The Right Care Starts with the Right Guidance",
    hero_subtitle: "Multilingual symptom triage, preliminary urgency assessment, and verified rural healthcare navigation for rural and semi-urban communities.",
    btn_check_symptoms: "Check My Symptoms",
    btn_find_healthcare: "Find Nearby Healthcare",
    feat_1_title: "Speak in Your Language",
    feat_1_desc: "Describe your symptoms via voice or text in Tamil, Hindi, or English. Designed for low-literacy and voice-first interaction.",
    feat_2_title: "Understand Your Care Urgency",
    feat_2_desc: "Validated clinical triage logic spots emergency red flags immediately, categorizing needs into Emergency, Urgent, or Routine.",
    feat_3_title: "Find Nearby Healthcare",
    feat_3_desc: "Interactive OpenStreetMap directory of Primary Health Centres, Community Health Centres, and Taluk Hospitals with emergency services.",
    step_1_title: "1. Describe Symptoms",
    step_1_desc: "Speak into the microphone or type how you feel in your preferred language.",
    step_2_title: "2. Review Urgency Guidance",
    step_2_desc: "See whether your condition requires immediate emergency care, prompt clinic evaluation, or routine home care.",
    step_3_title: "3. Find Appropriate Care",
    step_3_desc: "Get directions, contact numbers, and available services for the nearest appropriate government or charitable facility.",
    disclaimer_text: "MedPulse AI provides preliminary guidance, not a medical diagnosis. Consult a qualified healthcare professional.",

    // Assessment Page
    assess_page_title: "Symptom Reporting & Care Urgency Assessment",
    assess_page_desc: "Speak or type your symptoms in your preferred language. MedPulse AI uses validated clinical red-flag rules to provide preliminary triage guidance and match you with the appropriate healthcare facility.",
    label_choose_lang: "1. Choose Reporting Language",
    voice_status_ready: "Click microphone to speak symptoms",
    voice_status_supported: "Supports Tamil, Hindi, and English voice recognition.",
    label_describe_symptoms: "2. Describe How You Feel",
    symptoms_placeholder: "Describe symptoms here... For example: 'I have severe chest pain and breathlessness' or 'நெஞ்சு வலி மற்றும் மூச்சுத்திணறல்' or '4 दिन से तेज बुखार'",
    label_sample_prompts: "Or click a sample case to test:",
    label_age_group: "Age Group (Optional)",
    label_duration: "Duration (Optional)",
    label_context: "Medical Context / Preexisting Conditions (Optional)",
    context_placeholder: "e.g. Diabetes, Hypertension, Pregnancy, None",
    save_history_label: "Save to Private History: Keep this assessment record accessible in my local dashboard. (Unchecked by default for privacy).",
    btn_assess_urgency: "Assess Care Urgency",
    btn_reset_form: "Reset Form",
    results_empty_title: "Ready to Assess Your Symptoms",
    results_empty_desc: "Describe symptoms using the microphone or text box on the left, then click Assess Care Urgency. Your preliminary triage guidance will appear here.",
    opt_adult: "Adult (19 - 59 years)",
    opt_child: "Child (Under 12 years)",
    opt_teen: "Teenager (12 - 18 years)",
    opt_senior: "Senior (60+ years)",
    opt_dur_24h: "Less than 24 hours",
    opt_dur_1_3d: "1 to 3 days",
    opt_dur_4_7d: "4 to 7 days",
    opt_dur_1w: "More than a week",

    // Facilities Page
    fac_page_title: "Nearby Healthcare Resource Navigator",
    fac_page_desc: "Verified directory of Primary Health Centres (PHC), Community Health Centres (CHC), and Government Hospitals.",
    fac_search_placeholder: "Search village, town, district, or pin code (e.g. Melur, Madurai, 625106)",
    btn_use_location: "📍 Use My Location",
    filter_all: "All Facilities",
    filter_hospitals: "Hospitals",
    filter_chc: "Community Centres (CHC)",
    filter_phc: "Primary Centres (PHC)",
    filter_clinic: "Sub-Centres / Clinics",
    filter_emergency_toggle: "🚨 Only show facilities with 24/7 Emergency Care",

    // Dashboard Page
    dash_page_title: "Patient Health Dashboard",
    dash_page_desc: "Private assessment history, triage summaries, and personal privacy controls.",
    btn_new_assessment: "Start New Assessment",
    stat_total: "Total Assessments Recorded",
    stat_emergencies: "Emergency Red Flags Flagged",
    stat_urgent: "Urgent Cases Triaged",
    stat_routine: "Routine Consultations Guided",
    saved_history_title: "Saved Assessments History",
    btn_delete_all: "Delete All History",

    // Clinician Portal
    clinician_page_title: "Healthcare Professional Triage Review",
    clinician_page_desc: "Incoming multilingual patient triage summaries. High-priority Emergency cases are automatically pinned to the top.",
    doctor_on_duty_label: "Doctor On Duty: Dr. R. Sundaram, MD (Casualty Officer)",
    filter_queue_label: "Filter Triage Queue:",
    queue_filter_all: "All Cases",
    queue_filter_emerg: "Emergency Only (Red)",
    queue_filter_urgent: "Urgent Cases (Amber)",
    queue_filter_routine: "Routine Cases (Green)"
  },

  ta: {
    // Navigation
    nav_home: "முகப்பு",
    nav_symptoms: "அறிகுறி சோதனை",
    nav_facilities: "மருத்துவமனைகள்",
    nav_dashboard: "என் கணக்கு",
    nav_clinician: "மருத்துவர் பக்கம்",
    emergency_call_text: "அவசரமா? உடனே 108 / 112 அழையுங்கள்",

    // Landing Page
    hero_pill: "கிராமப்புற மற்றும் புறநகர் சுகாதார வழிகாட்டி",
    hero_title: "சரியான நேரத்தில் சரியான மருத்துவ வழிகாட்டல்",
    hero_subtitle: "தமிழ், இந்தி மற்றும் ஆங்கிலத்தில் உங்கள் அறிகுறிகளைப் பேசி அல்லது எழுதி தெரிந்து கொள்ளுங்கள். அவசரநிலையை உடனே கண்டறியுங்கள்.",
    btn_check_symptoms: "அறிகுறிகளைச் சோதிக்கவும்",
    btn_find_healthcare: "அருகிலுள்ள மருத்துவமனை",
    feat_1_title: "உங்கள் தாய்மொழியில் பேசுங்கள்",
    feat_1_desc: "மைக்ரோஃபோன் வழியாக தமிழில் பேசி அறிகுறிகளை எளிதாக பதிவு செய்யலாம். கிராமப்புற மக்களுக்கான குரல் வழி முறை.",
    feat_2_title: "அவசரநிலையை உணருங்கள்",
    feat_2_desc: "மருத்துவ அவசர சமிக்ஞைகளை உடனே கண்டறிந்து உரிய சிகிச்சை வழிகாட்டல் (அவசரம், விரைவு, அல்லது வழக்கமானது) வழங்கப்படுகிறது.",
    feat_3_title: "அருகிலுள்ள மருத்துவமனை அறிய",
    feat_3_desc: "ஆரம்ப சுகாதார நிலையங்கள், அரசு தாலுகா மருத்துவமனைகள் மற்றும் அவசர சிகிச்சை மையங்களை வரைபடத்தில் பாருங்கள்.",
    step_1_title: "1. அறிகுறிகளை கூறவும்",
    step_1_desc: "தமிழில் பேசவும் அல்லது உங்கள் உடல் நிலையை தட்டச்சு செய்யவும்.",
    step_2_title: "2. அவசரநிலையை அறியவும்",
    step_2_desc: "உடனடி அவசர சிகிச்சையா, ஒரு நாள் மருத்துவ ஆலோசனையா அல்லது எளிய பராமரிப்பா என்பதை அறியவும்.",
    step_3_title: "3. உரிய சிகிச்சையை அணுகவும்",
    step_3_desc: "அருகிலுள்ள அரசு மருத்துவமனையின் தொலைபேசி எண், பேருந்து வழி மற்றும் இருப்பிடத்தைப் பெறவும்.",
    disclaimer_text: "மெட்பல்ஸ் ஏஐ ஆரம்ப வழிகாட்டலை மட்டுமே வழங்குகிறது; இது மருத்துவ நோயறிதல் அல்ல. தகுதியான மருத்துவரை அணுகவும்.",

    // Assessment Page
    assess_page_title: "அறிகுறி பதிவு மற்றும் அவசரநிலை மதிப்பீடு",
    assess_page_desc: "உங்கள் தாய்மொழியில் பேசி அல்லது எழுதி அறிகுறிகளை பதிவு செய்யவும். மருத்துவ அவசர சமிக்ஞைகள் அடிப்படையில் உரிய சிகிச்சை வழிகாட்டல் உடனே கிடைக்கும்.",
    label_choose_lang: "1. மருத்துவ ஆலோசனை மொழியை தேர்வு செய்யவும்",
    voice_status_ready: "பேச மைக்ரோஃபோன் பொத்தானை அழுத்தவும்",
    voice_status_supported: "தமிழ், இந்தி மற்றும் ஆங்கிலக் குரல் பதிவை ஆதரிக்கிறது.",
    label_describe_symptoms: "2. உங்கள் உடல்நிலையை விவரிக்கவும்",
    symptoms_placeholder: "உங்கள் அறிகுறிகளை இங்கு விவரிக்கவும்... எ.கா: 'நெஞ்சு வலி மற்றும் மூச்சுத்திணறல்' அல்லது '4 நாட்களாக கடுமையான காய்ச்சல்'",
    label_sample_prompts: "அல்லது பரிசோதிக்க ஒரு உதாரணத்தை கிளிக் செய்யவும்:",
    label_age_group: "வயது பிரிவு (விரும்பினால்)",
    label_duration: "அறிகுறி காலம் (விரும்பினால்)",
    label_context: "மருத்துவ பின்னணி / முந்தைய நோய்கள் (விரும்பினால்)",
    context_placeholder: "எ.கா: சர்க்கரை நோய், ரத்த அழுத்தம், கர்ப்பம், எதுவுமில்லை",
    save_history_label: "தனிப்பட்ட வரலாற்றில் சேமிக்க: இந்த மதிப்பீட்டை என் டாஷ்போர்டில் சேமிக்கவும். (தனியுரிமைக்காக தானாக சேமிக்கப்படாது).",
    btn_assess_urgency: "அவசரநிலையை மதிப்பிடுங்கள்",
    btn_reset_form: "படிவத்தை மீட்டமை",
    results_empty_title: "அறிகுறிகளைச் சோதிக்க தயார்",
    results_empty_desc: "இடதுபுறத்தில் உள்ள மைக்ரோஃபோன் அல்லது பெட்டியில் அறிகுறிகளைக் குறிப்பிட்டு 'அவசரநிலையை மதிப்பிடுங்கள்' பொத்தானை அழுத்தவும்.",
    opt_adult: "பெரியவர் (19 - 59 ஆண்டுகள்)",
    opt_child: "குழந்தை (12 வயதுக்கு கீழ்)",
    opt_teen: "இளைஞர் (12 - 18 ஆண்டுகள்)",
    opt_senior: "முதியவர் (60+ ஆண்டுகள்)",
    opt_dur_24h: "24 மணி நேரத்திற்குள்",
    opt_dur_1_3d: "1 முதல் 3 நாட்கள்",
    opt_dur_4_7d: "4 முதல் 7 நாட்கள்",
    opt_dur_1w: "ஒரு வாரத்திற்கு மேல்",

    // Facilities Page
    fac_page_title: "அருகிலுள்ள அரசு மருத்துவ மைய வழிகாட்டி",
    fac_page_desc: "ஆரம்ப சுகாதார நிலையங்கள் (PHC), சமூக சுகாதார மையங்கள் (CHC) மற்றும் அரசு தாலுகா மருத்துவமனைகளின் சரிபார்க்கப்பட்ட பட்டியல்.",
    fac_search_placeholder: "கிராமம், நகரம், மாவட்டம் அல்லது அஞ்சல் குறியீட்டைத் தேடுங்கள் (எ.கா. மேலூர், மதுரை, 625106)",
    btn_use_location: "📍 என் இருப்பிடத்தைப் பயன்படுத்து",
    filter_all: "அனைத்து மையங்கள்",
    filter_hospitals: "மருத்துவமனைகள்",
    filter_chc: "சமூக மையங்கள் (CHC)",
    filter_phc: "ஆரம்ப நிலையங்கள் (PHC)",
    filter_clinic: "துணை மையங்கள் / கிளினிக்குகள்",
    filter_emergency_toggle: "🚨 24 மணி நேர அவசர சிகிச்சை மையங்களை மட்டும் காட்டு",

    // Dashboard Page
    dash_page_title: "நோயாளி சுகாதார டாஷ்போர்டு",
    dash_page_desc: "பாதுகாப்பான மதிப்பீட்டு வரலாறு மற்றும் தனிப்பட்ட தரவு கட்டுப்பாடு.",
    btn_new_assessment: "புதிய அறிகுறி சோதனை",
    stat_total: "மொத்த சோதனைகள்",
    stat_emergencies: "அவசர சமிக்ஞைகள்",
    stat_urgent: "விரைவான சிகிச்சை வழக்குகள்",
    stat_routine: "வழக்கமான ஆலோசனைகள்",
    saved_history_title: "சேமிக்கப்பட்ட மதிப்பீடுகள்",
    btn_delete_all: "அனைத்து வரலாற்றையும் அழி",

    // Clinician Portal
    clinician_page_title: "மருத்துவர் மற்றும் ஆஷா பணியாளர் பரிசீலனை தளம்",
    clinician_page_desc: "நோயாளிகளின் பன்மொழி மதிப்பீட்டு சுருக்கங்கள். அவசர வழக்குகள் முன்னுரிமை அடிப்படையில் வரிசைப்படுத்தப்படுகின்றன.",
    doctor_on_duty_label: "பணியில் உள்ள மருத்துவர்: டாக்டர் ஆர். சுந்தரம், MD (அவசர சிகிச்சை பிரிவு)",
    filter_queue_label: "வரிசையை வடிகட்டவும்:",
    queue_filter_all: "அனைத்து வழக்குகள்",
    queue_filter_emerg: "அவசர வழக்குகள் மட்டும் (சிவப்பு)",
    queue_filter_urgent: "விரைவு வழக்குகள் (மஞ்சள்)",
    queue_filter_routine: "வழக்கமான வழக்குகள் (பச்சை)"
  },

  hi: {
    // Navigation
    nav_home: "होम",
    nav_symptoms: "लक्षण जांच",
    nav_facilities: "निकटतम अस्पताल",
    nav_dashboard: "डैशबोर्ड",
    nav_clinician: "चिकित्सक पोर्टल",
    emergency_call_text: "आपातकाल? तुरंत 108 / 112 डायल करें",

    // Landing Page
    hero_pill: "ग्रामीण एवं अर्ध-शहरी स्वास्थ्य नेविगेशन",
    hero_title: "सही देखभाल की शुरुआत सही मार्गदर्शन से होती है",
    hero_subtitle: "अपनी भाषा में बोलकर या लिखकर लक्षणों की जांच करें। आपातकालीन संकेतों की तुरंत पहचान और निकटतम सरकारी अस्पतालों की जानकारी।",
    btn_check_symptoms: "अपने लक्षणों की जांच करें",
    btn_find_healthcare: "निकटतम अस्पताल खोजें",
    feat_1_title: "अपनी भाषा में बोलें",
    feat_1_desc: "हिंदी या अपनी भाषा में माइक के जरिए लक्षण बताएं। आवाज आधारित आसान सुविधा।",
    feat_2_title: "उपचार की तात्कालिकता समझें",
    feat_2_desc: "आपातकालीन रेड-फ्लैग चेतावनी और सही चिकित्सा स्तर (आपातकालीन, आवश्यक या सामान्य) की जानकारी।",
    feat_3_title: "निकटतम स्वास्थ्य केंद्र खोजें",
    feat_3_desc: "प्राथमिक स्वास्थ्य केंद्र (PHC), सामुदायिक स्वास्थ्य केंद्र (CHC) और जिला अस्पतालों की सूची व नक्शा।",
    step_1_title: "1. लक्षण बताएं",
    step_1_desc: "माइक बटन दबाकर बोलें या अपने लक्षणों को बॉक्स में लिखें।",
    step_2_title: "2. तात्कालिकता देखें",
    step_2_desc: "जांचें कि क्या तुरंत अस्पताल जाने की आवश्यकता है या सामान्य डॉक्टर परामर्श पर्याप्त है।",
    step_3_title: "3. सही स्वास्थ्य केंद्र पर जाएं",
    step_3_desc: "निकटतम केंद्र का पता, आपातकालीन नंबर और बस रूट की जानकारी प्राप्त करें।",
    disclaimer_text: "MedPulse AI केवल प्राथमिक मार्गदर्शन प्रदान करता है, यह चिकित्सकीय निदान नहीं है। डॉक्टर से परामर्श लें।",

    // Assessment Page
    assess_page_title: "लक्षण रिपोर्टिंग एवं तात्कालिकता मूल्यांकन",
    assess_page_desc: "अपनी पसंदीदा भाषा में बोलकर या लिखकर लक्षण दर्ज करें। क्लिनिकल नियमों के आधार पर तात्कालिकता की जांच और सही अस्पताल का सुझाव तुरंत पाएं।",
    label_choose_lang: "1. परामर्श की भाषा चुनें",
    voice_status_ready: "लक्षण बोलने के लिए माइक दबाएं",
    voice_status_supported: "तमिल, हिंदी और अंग्रेजी आवाज पहचान समर्थित है।",
    label_describe_symptoms: "2. बताएं कि आप कैसा महसूस कर रहे हैं",
    symptoms_placeholder: "अपने लक्षण यहां लिखें... जैसे: 'सीने में तेज दर्द और सांस फूलना' या '4 दिन से तेज बुखार'",
    label_sample_prompts: "या परीक्षण के लिए कोई उदाहरण चुनें:",
    label_age_group: "आयु वर्ग (वैकल्पिक)",
    label_duration: "अवधि (वैकल्पिक)",
    label_context: "चिकित्सा इतिहास / पुरानी बीमारियां (वैकल्पिक)",
    context_placeholder: "जैसे: मधुमेह, उच्च रक्तचाप, गर्भावस्था, कोई नहीं",
    save_history_label: "निजी इतिहास में सहेजें: इस रिकॉर्ड को स्थानीय डैशबोर्ड में सुरक्षित रखें। (गोपनीयता के लिए डिफ़ॉल्ट रूप से बंद)।",
    btn_assess_urgency: "तात्कालिकता का आकलन करें",
    btn_reset_form: "फॉर्म रीसेट करें",
    results_empty_title: "लक्षण जांच के लिए तैयार",
    results_empty_desc: "बाईं ओर माइक या टेक्स्ट बॉक्स से लक्षण बताएं और 'तात्कालिकता का आकलन करें' पर क्लिक करें।",
    opt_adult: "वयस्क (19 - 59 वर्ष)",
    opt_child: "बच्चा (12 वर्ष से कम)",
    opt_teen: "किशोर (12 - 18 वर्ष)",
    opt_senior: "वरिष्ठ नागरिक (60+ वर्ष)",
    opt_dur_24h: "24 घंटे से कम",
    opt_dur_1_3d: "1 से 3 दिन",
    opt_dur_4_7d: "4 से 7 दिन",
    opt_dur_1w: "एक सप्ताह से अधिक",

    // Facilities Page
    fac_page_title: "निकटतम स्वास्थ्य संसाधन नेविगेटर",
    fac_page_desc: "प्राथमिक स्वास्थ्य केंद्र (PHC), सामुदायिक स्वास्थ्य केंद्र (CHC) और सरकारी अस्पतालों की सत्यापित सूची।",
    fac_search_placeholder: "गांव, कस्बा, जिला या पिन कोड खोजें (उदा. मेलूर, मदुरै, 625106)",
    btn_use_location: "📍 मेरे स्थान का उपयोग करें",
    filter_all: "सभी केंद्र",
    filter_hospitals: "अस्पताल",
    filter_chc: "सामुदायिक केंद्र (CHC)",
    filter_phc: "प्राथमिक केंद्र (PHC)",
    filter_clinic: "उप-स्वास्थ्य केंद्र / क्लीनिक",
    filter_emergency_toggle: "🚨 केवल 24/7 आपातकालीन सेवा वाले केंद्र दिखाएं",

    // Dashboard Page
    dash_page_title: "मरीज स्वास्थ्य डैशबोर्ड",
    dash_page_desc: "सुरक्षित मूल्यांकन इतिहास एवं निजी डेटा नियंत्रण।",
    btn_new_assessment: "नया परीक्षण शुरू करें",
    stat_total: "कुल दर्ज मूल्यांकन",
    stat_emergencies: "आपातकालीन रेड-फ्लैग",
    stat_urgent: "शीघ्र आवश्यक मामले",
    stat_routine: "सामान्य परामर्श",
    saved_history_title: "सहेजे गए मूल्यांकन",
    btn_delete_all: "संपूर्ण इतिहास मिटाएं",

    // Clinician Portal
    clinician_page_title: "चिकित्सक एवं आशा कार्यकर्ता समीक्षा पोर्टल",
    clinician_page_desc: "प्राथमिकता के आधार पर आने वाले मरीजों के बहुभाषी सारांश। आपातकालीन मामले स्वतः सबसे ऊपर रहते हैं।",
    doctor_on_duty_label: "ड्यूटी पर डॉक्टर: डॉ. आर. सुंदरम, MD (इमरजेंसी अधिकारी)",
    filter_queue_label: "कतार को फ़िल्टर करें:",
    queue_filter_all: "सभी मामले",
    queue_filter_emerg: "केवल आपातकालीन (लाल)",
    queue_filter_urgent: "आवश्यक मामले (पीला)",
    queue_filter_routine: "सामान्य मामले (हरा)"
  }
};

function getCurrentLanguage() {
  return localStorage.getItem('medpulse_lang') || 'en';
}

function setCurrentLanguage(lang) {
  if (['en', 'ta', 'hi'].includes(lang)) {
    localStorage.setItem('medpulse_lang', lang);
    applyTranslations(lang);
    
    // Also notify any listening components
    window.dispatchEvent(new CustomEvent('medpulse_language_changed', { detail: { language: lang } }));
  }
}

function applyTranslations(lang) {
  const dict = I18N_DICTIONARY[lang] || I18N_DICTIONARY.en;
  
  // Translate text content
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Translate placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Sync global select dropdown
  const langSelect = document.getElementById('global-lang-select');
  if (langSelect && langSelect.value !== lang) {
    langSelect.value = lang;
  }
  
  // Sync assessment language selector if on assessment page
  const assessLangSelect = document.getElementById('assessment-lang-select');
  if (assessLangSelect && assessLangSelect.value !== lang) {
    assessLangSelect.value = lang;
  }
}

// Mobile navigation toggle
function setupMobileMenu() {
  const btn = document.querySelector('.mobile-menu-btn');
  const links = document.querySelector('.nav-links');
  if (btn && links) {
    btn.addEventListener('click', () => {
      links.classList.toggle('show');
    });
  }
}

// Health status check badge
async function checkBackendConnectivity() {
  const healthBadge = document.getElementById('backend-status-badge');
  if (!healthBadge) return;
  
  const health = await api.getHealth();
  if (health.status === 'healthy') {
    healthBadge.innerHTML = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10B981;margin-right:6px;"></span>Backend Online (${health.database})`;
    healthBadge.style.color = '#065F46';
  } else {
    healthBadge.innerHTML = `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#F59E0B;margin-right:6px;"></span>Demo Mode (Offline)`;
    healthBadge.style.color = '#92400E';
  }
}

// Text-to-Speech Accessibility Helper (Web Speech API)
function speakText(text, lang = 'en') {
  if (!('speechSynthesis' in window)) {
    if (typeof showToast === 'function') {
      showToast("Speech synthesis not supported in this browser.", "error");
    }
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  const localeMap = { en: 'en-IN', ta: 'ta-IN', hi: 'hi-IN' };
  utterance.lang = localeMap[lang] || 'en-IN';
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  setupMobileMenu();
  
  const langSelect = document.getElementById('global-lang-select');
  if (langSelect) {
    langSelect.value = getCurrentLanguage();
    langSelect.addEventListener('change', (e) => {
      setCurrentLanguage(e.target.value);
    });
  }

  applyTranslations(getCurrentLanguage());
  checkBackendConnectivity();
});
