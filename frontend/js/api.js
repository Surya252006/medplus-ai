// MedPulse AI — Centralized API Client

const API_BASE = (window.location.protocol.startsWith('http') && window.location.port === '8000')
  ? '' 
  : (localStorage.getItem('MEDPULSE_API_URL') || 'http://localhost:8000');

const api = {
  async getHealth() {
    try {
      const res = await fetch(`${API_BASE}/api/health`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Backend health check failed:", err);
      return { status: "offline", error: err.message };
    }
  },

  async getLanguages() {
    try {
      const res = await fetch(`${API_BASE}/api/languages`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn("Using fallback language list:", err);
      return [
        { code: "en", name: "English", native: "English", voice_locale: "en-IN", flag: "🇬🇧" },
        { code: "ta", name: "Tamil", native: "தமிழ்", voice_locale: "ta-IN", flag: "🇮🇳" },
        { code: "hi", name: "Hindi", native: "हिन्दी", voice_locale: "hi-IN", flag: "🇮🇳" }
      ];
    }
  },

  async submitTriage(data) {
    const res = await fetch(`${API_BASE}/api/triage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Server error (${res.status})`);
    }
    return await res.json();
  },

  async translate(text, sourceLang = "auto") {
    const res = await fetch(`${API_BASE}/api/translate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, source_lang: sourceLang })
    });
    if (!res.ok) throw new Error(`Translation error (${res.status})`);
    return await res.json();
  },

  async generateSummary(data) {
    const res = await fetch(`${API_BASE}/api/summary`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Summary generation error (${res.status})`);
    return await res.json();
  },

  async getFacilities(params = {}) {
    try {
      const query = new URLSearchParams();
      if (params.query) query.append('query', params.query);
      if (params.category && params.category !== 'ALL') query.append('category', params.category);
      if (params.emergency_only) query.append('emergency_only', 'true');
      if (params.lat !== undefined && params.lon !== undefined) {
        query.append('lat', params.lat);
        query.append('lon', params.lon);
      }
      const res = await fetch(`${API_BASE}/api/facilities?${query.toString()}`);
      if (res.ok) return await res.json();
      throw new Error(`Facilities API error: ${res.status}`);
    } catch (err) {
      console.warn("Falling back to static facilities dataset:", err);
      // Fallback for static hosting
      const res = await fetch('/data/sample_facilities.json');
      let facilities = await res.json();
      if (params.category && params.category !== 'ALL') {
        facilities = facilities.filter(f => f.category === params.category);
      }
      if (params.emergency_only) {
        facilities = facilities.filter(f => f.emergency_services);
      }
      if (params.query) {
        const q = params.query.toLowerCase();
        facilities = facilities.filter(f => f.name.toLowerCase().includes(q) || f.address.toLowerCase().includes(q));
      }
      return facilities;
    }
  },

  async getFacilityDetail(facilityId) {
    try {
      const res = await fetch(`${API_BASE}/api/facilities/${facilityId}`);
      if (res.ok) return await res.json();
      throw new Error(`Facility fetch error`);
    } catch (err) {
      const facilities = await this.getFacilities();
      return facilities.find(f => f.id === facilityId) || null;
    }
  },

  async getAssessments() {
    try {
      const res = await fetch(`${API_BASE}/api/assessments`);
      if (res.ok) return await res.json();
      throw new Error(`HTTP ${res.status}`);
    } catch (err) {
      console.warn("Assessments API offline, reading local cache");
      return JSON.parse(localStorage.getItem('medpulse_assessments_cache') || '[]');
    }
  },

  async deleteAssessment(id) {
    const res = await fetch(`${API_BASE}/api/assessments/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error(`Delete failed (${res.status})`);
    return await res.json();
  },

  async clearAllAssessments() {
    const res = await fetch(`${API_BASE}/api/assessments`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error(`Purge failed (${res.status})`);
    return await res.json();
  },

  async getClinicianQueue() {
    const res = await fetch(`${API_BASE}/api/clinician/queue`);
    if (!res.ok) throw new Error(`Queue fetch error (${res.status})`);
    return await res.json();
  },

  async clinicianAcknowledge(assessmentId, notes = "") {
    const res = await fetch(`${API_BASE}/api/clinician/acknowledge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        assessment_id: assessmentId,
        clinician_notes: notes
      })
    });
    if (!res.ok) throw new Error(`Acknowledgment failed (${res.status})`);
    return await res.json();
  }
};

// UI Toast Notification Helper
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span>${message}</span>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
