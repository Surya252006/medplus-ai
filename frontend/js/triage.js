// MedPulse AI — Symptom Assessment Controller (Voice, Triage, Structured Summary)

let recognitionInstance = null;
let isRecording = false;

// Initialize Speech Recognition with Multilingual Support
function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const micBtn = document.getElementById('mic-btn');
  const micTitle = document.getElementById('voice-status-title');
  const micDesc = document.getElementById('voice-status-desc');
  const symptomInput = document.getElementById('symptoms-input');

  if (!SpeechRecognition) {
    if (micTitle) micTitle.textContent = "Voice input unsupported in this browser";
    if (micDesc) micDesc.textContent = "Please type your symptoms directly in the text box below.";
    if (micBtn) {
      micBtn.style.opacity = '0.5';
      micBtn.title = "Voice recognition not supported in your browser";
      micBtn.onclick = () => {
        showToast("Speech recognition is not supported in this browser. Please type your symptoms.", "error");
      };
    }
    return;
  }

  recognitionInstance = new SpeechRecognition();
  recognitionInstance.continuous = false;
  recognitionInstance.interimResults = false;

  recognitionInstance.onstart = () => {
    isRecording = true;
    micBtn.classList.add('listening');
    const lang = document.getElementById('assessment-lang-select')?.value || 'en';
    const langNames = { en: "English", ta: "Tamil (தமிழ்)", hi: "Hindi (हिन्दी)" };
    micTitle.textContent = `Listening in ${langNames[lang] || lang}...`;
    micDesc.textContent = "Please speak clearly into your microphone.";
  };

  recognitionInstance.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    if (symptomInput) {
      if (symptomInput.value.trim()) {
        symptomInput.value = `${symptomInput.value.trim()} ${transcript}`;
      } else {
        symptomInput.value = transcript;
      }
    }
    showToast("Voice input captured successfully!", "success");
  };

  recognitionInstance.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    isRecording = false;
    micBtn.classList.remove('listening');
    micTitle.textContent = "Voice recognition paused";
    if (event.error === 'not-allowed') {
      micDesc.textContent = "Microphone access blocked. Please permit microphone or type symptoms manually.";
      showToast("Microphone permission denied. You can type symptoms below.", "error");
    } else {
      micDesc.textContent = "No speech detected. Click mic to try again or type manually.";
    }
  };

  recognitionInstance.onend = () => {
    isRecording = false;
    micBtn.classList.remove('listening');
    const micTitle = document.getElementById('voice-status-title');
    const micDesc = document.getElementById('voice-status-desc');
    if (micTitle) micTitle.textContent = "Click microphone to speak";
    if (micDesc) micDesc.textContent = "Supports English, Tamil (தமிழ்), and Hindi (हिन्दी)";
  };

  micBtn.onclick = toggleRecording;
}

function toggleRecording() {
  if (!recognitionInstance) {
    showToast("Voice input is not available on this browser.", "error");
    return;
  }

  if (isRecording) {
    recognitionInstance.stop();
  } else {
    const lang = document.getElementById('assessment-lang-select')?.value || 'en';
    const localeMap = {
      en: 'en-IN',
      ta: 'ta-IN',
      hi: 'hi-IN'
    };
    recognitionInstance.lang = localeMap[lang] || 'en-US';
    try {
      recognitionInstance.start();
    } catch (e) {
      console.warn("Recognition start failed:", e);
    }
  }
}

// Prompt Chip Click Handler
function setupPromptChips() {
  document.querySelectorAll('.prompt-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const text = chip.getAttribute('data-text');
      const lang = chip.getAttribute('data-lang');
      const input = document.getElementById('symptoms-input');
      const langSelect = document.getElementById('assessment-lang-select');
      
      if (input && text) {
        input.value = text;
        input.focus();
      }
      if (langSelect && lang) {
        langSelect.value = lang;
        if (typeof setCurrentLanguage === 'function') {
          setCurrentLanguage(lang);
        }
      }
    });
  });
}

// Submit Triage
async function handleTriageSubmit(e) {
  if (e) e.preventDefault();
  
  const symptomsText = document.getElementById('symptoms-input')?.value.trim();
  if (!symptomsText || symptomsText.length < 3) {
    showToast("Please enter or speak your symptoms first.", "error");
    document.getElementById('symptoms-input')?.focus();
    return;
  }

  const lang = document.getElementById('assessment-lang-select')?.value || 'en';
  const ageGroup = document.getElementById('age-group-select')?.value || 'adult';
  const duration = document.getElementById('duration-select')?.value || '';
  const context = document.getElementById('context-input')?.value.trim() || '';
  const saveConsent = document.getElementById('save-history-consent')?.checked || false;

  const submitBtn = document.getElementById('submit-assessment-btn');
  const originalBtnHtml = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = `
    <svg style="animation: spin 1s linear infinite; width:18px; height:18px; display:inline-block;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
      <circle cx="12" cy="12" r="10" stroke-width="4" stroke="currentColor" opacity="0.3"></circle>
      <path d="M4 12a8 8 0 018-8" stroke-width="4" stroke="currentColor"></path>
    </svg>
    Analyzing Symptoms...
  `;

  try {
    const payload = {
      symptoms_text: symptomsText,
      language: lang,
      age_group: ageGroup,
      duration: duration,
      additional_context: context,
      save_to_history: saveConsent
    };

    const triageResult = await api.submitTriage(payload);
    renderTriageResult(triageResult, payload);

    // Also fetch structured medical summary
    const summaryReq = {
      symptoms_text: symptomsText,
      translated_text: triageResult.translated_symptoms,
      language: lang,
      age_group: ageGroup,
      duration: duration,
      additional_context: context,
      urgency_category: triageResult.urgency_category,
      recognized_symptoms: triageResult.recognized_symptoms,
      red_flags_detected: triageResult.red_flags_detected,
      recommended_action: triageResult.recommended_action,
      recommended_facility_type: triageResult.recommended_facility_type
    };

    const summaryResult = await api.generateSummary(summaryReq);
    renderMedicalSummary(summaryResult);

    if (triageResult.assessment_id) {
      showToast(`Assessment saved to private history (ID: ${triageResult.assessment_id})`, "success");
    }

    // Smooth scroll to result
    const resultsContainer = document.getElementById('results-panel');
    if (resultsContainer) {
      resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

  } catch (err) {
    console.error("Triage submission error:", err);
    showToast(`Assessment failed: ${err.message}`, "error");
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalBtnHtml;
  }
}

// Render Triage Results Card
function renderTriageResult(res, reqPayload) {
  const panel = document.getElementById('results-panel');
  if (!panel) return;

  const categoryLower = res.urgency_category.toLowerCase();
  
  let iconSvg = '';
  if (categoryLower === 'emergency') {
    iconSvg = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
  } else if (categoryLower === 'urgent') {
    iconSvg = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
  } else {
    iconSvg = `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`;
  }

  // Facility category link
  let facilityCategory = 'ALL';
  if (categoryLower === 'emergency') facilityCategory = 'HOSPITAL';
  else if (categoryLower === 'urgent') facilityCategory = 'CHC';
  else facilityCategory = 'PHC';

  // Use localized content if available
  const displayTitle = res.localized_urgency_title || res.urgency_title;
  const displayExplanation = res.localized_explanation || res.explanation;
  const displayAction = res.localized_action || res.recommended_action;
  const displayWarnings = (res.localized_warnings && res.localized_warnings.length > 0) ? res.localized_warnings : (res.safety_warnings || []);
  const lang = reqPayload.language || 'en';
  
  const speechText = `${displayTitle}. ${displayExplanation}. ${displayAction}`.replace(/['"\\]/g, ' ');

  panel.innerHTML = `
    <!-- Urgency Status Banner -->
    <div class="urgency-badge-banner ${categoryLower}">
      <div class="urgency-icon-circle">
        ${iconSvg}
      </div>
      <div class="urgency-title-text" style="flex: 1;">
        <h3>${displayTitle}</h3>
        <p>${displayExplanation}</p>
        <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
          <button type="button" class="btn btn-outline btn-sm" onclick="speakText('${speechText}', '${lang}')" style="background: rgba(255,255,255,0.95); font-weight: 700; color: var(--text-main); display: inline-flex; align-items: center; gap: 6px;" title="Listen to triage guidance spoken aloud">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
            <span>🔊 Listen to Guidance</span>
          </button>
          ${categoryLower === 'emergency' ? `
            <a href="tel:108" class="btn btn-danger btn-sm" style="display: inline-flex; align-items: center; gap: 6px; font-weight: 800;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
              <span>Call 108 Ambulance</span>
            </a>
          ` : ''}
        </div>
      </div>
    </div>

    <!-- Red Flag Box if Emergency -->
    ${res.red_flags_detected && res.red_flags_detected.length > 0 ? `
      <div class="red-flag-alert">
        <h5>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          Emergency Red Flags Detected
        </h5>
        <ul>
          ${res.red_flags_detected.map(rf => `<li>${rf}</li>`).join('')}
        </ul>
      </div>
    ` : ''}

    <!-- Recommended Action & Level of Care -->
    <div class="card" style="margin-bottom: 1.25rem; border-left: 4px solid ${res.urgency_color};">
      <h4 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 8px;">Recommended Care Action</h4>
      <p style="font-size: 0.95rem; color: var(--text-main); line-height: 1.5; margin-bottom: 12px;">
        ${displayAction}
      </p>

      <div style="background: var(--surface-alt); padding: 10px 14px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
        <div>
          <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Appropriate Facility Level:</span>
          <div style="font-weight: 700; color: var(--text-main); font-size: 0.95rem;">${res.recommended_facility_type}</div>
        </div>
        <a href="facilities.html?category=${facilityCategory}" class="btn btn-primary btn-sm">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
          Find Matching Facilities
        </a>
      </div>
    </div>

    <!-- Recognized Clinical Concepts & Rules -->
    <div class="card" style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 8px;">Clinical Concept Recognition</h4>
      <div class="tags-row">
        ${res.recognized_symptoms.map(s => `<span class="tag-item">${s}</span>`).join('')}
      </div>
      <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 10px;">
        <strong>Clinical Rationale:</strong> ${res.clinical_rationale}
      </div>
      ${res.translated_symptoms && res.translated_symptoms !== reqPayload.symptoms_text ? `
        <div style="font-size: 0.85rem; color: var(--secondary); margin-top: 6px; background: var(--secondary-light); padding: 6px 10px; border-radius: var(--radius-sm);">
          <strong>Multilingual Translation:</strong> ${res.translated_symptoms}
        </div>
      ` : ''}
    </div>

    <!-- Safety Warnings -->
    ${displayWarnings && displayWarnings.length > 0 ? `
      <div style="background: var(--surface); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem 1.25rem; margin-bottom: 1.25rem;">
        <h5 style="font-size: 0.9rem; font-weight: 700; color: var(--text-main); margin-bottom: 6px;">Important Safety Instructions:</h5>
        <ul style="padding-left: 1.25rem; font-size: 0.875rem; color: var(--text-muted);">
          ${displayWarnings.map(w => `<li>${w}</li>`).join('')}
        </ul>
      </div>
    ` : ''}

    <!-- Structured Medical Summary Slot -->
    <div id="medical-summary-container"></div>

    <!-- Clinical Disclaimer -->
    <div class="clinical-disclaimer-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      <div>${res.disclaimer}</div>
    </div>
  `;
}

// Render Structured Medical Summary (Section 4.D)
function renderMedicalSummary(summary) {
  const container = document.getElementById('medical-summary-container');
  if (!container) return;

  container.innerHTML = `
    <div class="medical-summary-box">
      <div class="medical-summary-header">
        <div>
          <h4>Structured Medical Summary for Healthcare Provider</h4>
          <span style="font-size: 0.775rem; color: var(--text-muted);">ID: ${summary.summary_id} • Generated: ${summary.generated_at}</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button type="button" class="btn btn-outline btn-sm" onclick="copyMedicalSummary()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            Copy
          </button>
          <button type="button" class="btn btn-outline btn-sm" onclick="window.print()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Print
          </button>
        </div>
      </div>

      <div class="summary-field">
        <div class="summary-label">Patient Reported Chief Complaint</div>
        <textarea id="summary-chief-complaint" class="summary-editable-textarea" rows="2">${summary.chief_complaint}</textarea>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 0.85rem;">
        <div class="summary-field">
          <div class="summary-label">Reported Duration</div>
          <input type="text" id="summary-duration" class="form-control" style="min-height: 38px; padding: 6px 10px; font-size: 0.85rem;" value="${summary.duration}">
        </div>
        <div class="summary-field">
          <div class="summary-label">Age Group / Demographics</div>
          <input type="text" id="summary-age" class="form-control" style="min-height: 38px; padding: 6px 10px; font-size: 0.85rem;" value="${summary.age_group}">
        </div>
      </div>

      <div class="summary-field">
        <div class="summary-label">Pertinent Negatives & Missing Information</div>
        <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: var(--radius-sm); padding: 8px 12px; font-size: 0.825rem; color: #92400E;">
          ${summary.pertinent_negatives && summary.pertinent_negatives.length > 0 ? `
            <ul style="padding-left: 1rem; margin: 0;">
              ${summary.pertinent_negatives.map(m => `<li>${m}</li>`).join('')}
            </ul>
          ` : 'No major diagnostic gaps detected.'}
        </div>
      </div>

      <div class="summary-field">
        <div class="summary-label">Triage Recommendation & Level of Care</div>
        <div class="summary-value" style="font-weight: 700;">
          ${summary.urgency_assessment} — ${summary.recommended_level_of_care}
        </div>
      </div>

      <div style="margin-top: 10px; font-size: 0.775rem; color: var(--text-muted); font-style: italic;">
        * Note: You may edit the fields above to adjust details before showing this note to your doctor or ASHA health worker.
      </div>
    </div>
  `;
}

// Copy Summary to Clipboard
function copyMedicalSummary() {
  const complaint = document.getElementById('summary-chief-complaint')?.value || '';
  const duration = document.getElementById('summary-duration')?.value || '';
  const age = document.getElementById('summary-age')?.value || '';
  
  const textToCopy = `MedPulse AI — Structured Patient Medical Summary\n\nChief Complaint: ${complaint}\nDuration: ${duration}\nAge Group: ${age}\n\nNotice: Preliminary guidance for clinical review.`;
  
  navigator.clipboard.writeText(textToCopy).then(() => {
    showToast("Summary copied to clipboard!", "success");
  }).catch(() => {
    showToast("Unable to copy to clipboard", "error");
  });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initSpeechRecognition();
  setupPromptChips();

  const form = document.getElementById('assessment-form');
  if (form) {
    form.addEventListener('submit', handleTriageSubmit);
  }

  const resetBtn = document.getElementById('reset-assessment-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      document.getElementById('symptoms-input').value = '';
      document.getElementById('context-input').value = '';
      const resultsContainer = document.getElementById('results-panel');
      if (resultsContainer) {
        resultsContainer.innerHTML = `
          <div class="card" style="text-align: center; padding: 3rem 1.5rem; color: var(--text-muted);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin: 0 auto 1rem; opacity: 0.4;"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
            <h4 style="font-weight: 700; color: var(--text-main); margin-bottom: 6px;">No Assessment Submitted Yet</h4>
            <p style="font-size: 0.9rem;">Describe your symptoms using the microphone or text box on the left, then click <strong>Assess Care Urgency</strong>.</p>
          </div>
        `;
      }
    });
  }
});
