// MedPulse AI — Healthcare Resource Navigator (Leaflet + OpenStreetMap)

let map = null;
let markersLayer = null;
let userMarker = null;
let allFacilities = [];
let userLocation = null;

// Initialize Leaflet Map
function initMap() {
  const mapContainer = document.getElementById('leaflet-map');
  if (!mapContainer || map) return;

  // Center around rural Madurai/Melur district belt
  map = L.map('leaflet-map').setView([10.0286, 78.25], 11);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  markersLayer = L.layerGroup().addTo(map);
}

// Marker Icon Helper
function createCustomMarkerIcon(category, isEmergency) {
  let color = '#0D9488'; // default teal PHC
  if (category === 'HOSPITAL') color = '#EF4444'; // Red
  else if (category === 'CHC') color = '#F59E0B'; // Amber
  else if (category === 'CLINIC') color = '#0284C7'; // Blue

  const html = `
    <div style="
      background-color: ${color};
      width: 32px;
      height: 32px;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      border: 2px solid #FFFFFF;
      box-shadow: 0 3px 6px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
    ">
      <div style="
        width: 12px;
        height: 12px;
        background: #FFFFFF;
        border-radius: 50%;
        transform: rotate(45deg);
      "></div>
    </div>
  `;

  return L.divIcon({
    className: 'custom-map-pin',
    html: html,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -30]
  });
}

// Load and Render Facilities
async function loadFacilities(params = {}) {
  const listContainer = document.getElementById('facility-list-container');
  if (listContainer) {
    listContainer.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
        <svg style="animation: spin 1s linear infinite; width:24px; height:24px; margin-bottom:8px;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" stroke-width="4" stroke="currentColor" opacity="0.3"></circle>
          <path d="M4 12a8 8 0 018-8" stroke-width="4" stroke="currentColor"></path>
        </svg>
        <p>Loading verified healthcare facilities...</p>
      </div>
    `;
  }

  try {
    const data = await api.getFacilities(params);
    allFacilities = data.facilities || [];
    renderFacilitiesList(allFacilities);
    renderMapMarkers(allFacilities);

    const countElem = document.getElementById('facility-count');
    if (countElem) {
      countElem.textContent = `${allFacilities.length} facilities found`;
    }
  } catch (err) {
    console.error("Facilities load error:", err);
    if (listContainer) {
      listContainer.innerHTML = `
        <div class="card" style="text-align: center; padding: 2rem; color: var(--emergency-color);">
          <p>Unable to load facility directory. Please check your connection.</p>
        </div>
      `;
    }
  }
}

// Render Facility Cards in List View
function renderFacilitiesList(facilities) {
  const container = document.getElementById('facility-list-container');
  if (!container) return;

  if (facilities.length === 0) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 2.5rem 1rem; color: var(--text-muted);">
        <p style="font-weight: 700; margin-bottom: 6px;">No matching healthcare facilities found.</p>
        <p style="font-size: 0.875rem;">Try adjusting your search query, village/pincode, or category filter.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = facilities.map(fac => {
    let catBadgeClass = 'badge-phc';
    if (fac.category === 'HOSPITAL') catBadgeClass = 'badge-hospital';
    else if (fac.category === 'CHC') catBadgeClass = 'badge-chc';
    else if (fac.category === 'CLINIC') catBadgeClass = 'badge-clinic';

    return `
      <div class="facility-card-item" id="card-${fac.id}" onclick="selectFacility('${fac.id}')">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-bottom: 6px;">
          <div>
            <span class="facility-type-badge ${catBadgeClass}">${fac.type}</span>
            ${fac.is_24x7_emergency ? `
              <span style="display: inline-block; background: #DC2626; color: #fff; padding: 2px 7px; border-radius: var(--radius-sm); font-size: 0.7rem; font-weight: 700; margin-left: 4px;">
                24/7 EMERGENCY
              </span>
            ` : ''}
          </div>
          ${fac.distance_km !== null ? `
            <span class="distance-tag">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
              ${fac.distance_km} km
            </span>
          ` : ''}
        </div>

        <h3 style="font-size: 1.05rem; font-weight: 800; color: var(--text-main); margin-bottom: 4px;">
          ${fac.name}
        </h3>
        
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline; margin-right:4px;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
          ${fac.address} (PIN: ${fac.pincode})
        </p>

        <div style="font-size: 0.825rem; color: var(--text-main); margin-bottom: 6px;">
          <strong>Doctor Availability:</strong> ${fac.doctor_availability}
        </div>

        <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 10px;">
          <strong>Transport:</strong> ${fac.transport_info}
        </div>

        <div class="tags-row" style="margin-bottom: 12px;">
          ${fac.services.slice(0, 4).map(s => `<span class="tag-item" style="font-size: 0.75rem;">${s}</span>`).join('')}
          ${fac.services.length > 4 ? `<span class="tag-item" style="font-size: 0.75rem;">+${fac.services.length - 4} more</span>` : ''}
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; border-top: 1px solid var(--border-color); padding-top: 10px;">
          <a href="tel:${fac.emergency_phone.split('/')[0].trim()}" class="btn btn-danger btn-sm" onclick="event.stopPropagation();">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
            Call Facility
          </a>
          <a href="https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=${userLocation ? `${userLocation.lat},${userLocation.lon}` : ''}%3B${fac.latitude},${fac.longitude}" target="_blank" rel="noopener" class="btn btn-outline btn-sm" onclick="event.stopPropagation();">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            Get Directions
          </a>
          <button type="button" class="btn btn-secondary btn-sm" onclick="event.stopPropagation(); focusMapOn('${fac.id}');">
            View on Map
          </button>
        </div>
      </div>
    `;
  }).join('');
}

// Render Markers on Map
function renderMapMarkers(facilities) {
  if (!map || !markersLayer) return;

  markersLayer.clearLayers();
  const bounds = L.latLngBounds();

  facilities.forEach(fac => {
    const lat = fac.latitude;
    const lon = fac.longitude;
    bounds.extend([lat, lon]);

    const icon = createCustomMarkerIcon(fac.category, fac.is_24x7_emergency);
    const marker = L.marker([lat, lon], { icon: icon }).addTo(markersLayer);

    const popupHtml = `
      <div style="font-family: inherit; max-width: 240px; padding: 4px;">
        <div style="font-size: 0.75rem; font-weight: 700; color: var(--primary); text-transform: uppercase;">${fac.type}</div>
        <h4 style="font-size: 0.95rem; font-weight: 800; margin: 3px 0 6px;">${fac.name}</h4>
        <div style="font-size: 0.8rem; color: #475569; margin-bottom: 6px;">${fac.address}</div>
        <div style="font-size: 0.8rem; font-weight: 600; color: #0F172A; margin-bottom: 8px;">
          📞 ${fac.phone}
        </div>
        <div style="display: flex; gap: 6px;">
          <a href="tel:${fac.phone}" style="background: #0D9488; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; text-decoration: none; font-weight: 600;">Call</a>
          <button onclick="selectFacility('${fac.id}')" style="background: #F1F5F9; border: 1px solid #CBD5E1; color: #0F172A; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; cursor: pointer;">Details</button>
        </div>
      </div>
    `;

    marker.bindPopup(popupHtml);
    marker.on('click', () => {
      highlightFacilityCard(fac.id);
    });

    fac._marker = marker;
  });

  if (facilities.length > 0 && !userLocation) {
    map.fitBounds(bounds, { padding: [40, 40] });
  }
}

// Select Facility
function selectFacility(facilityId) {
  highlightFacilityCard(facilityId);
  focusMapOn(facilityId);
}

function highlightFacilityCard(facilityId) {
  document.querySelectorAll('.facility-card-item').forEach(c => c.classList.remove('active'));
  const card = document.getElementById(`card-${facilityId}`);
  if (card) {
    card.classList.add('active');
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function focusMapOn(facilityId) {
  const fac = allFacilities.find(f => f.id === facilityId);
  if (fac && map) {
    map.flyTo([fac.latitude, fac.longitude], 14, { duration: 1.2 });
    if (fac._marker) {
      fac._marker.openPopup();
    }
  }
}

// Geolocation Handling
function requestUserLocation() {
  const btn = document.getElementById('btn-get-location');
  if (!navigator.geolocation) {
    showToast("Geolocation is not supported by your browser.", "error");
    return;
  }

  if (btn) btn.innerHTML = `<span>Detecting Location...</span>`;

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      userLocation = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude
      };

      if (btn) btn.innerHTML = `<span>📍 Location Active</span>`;
      showToast("Found your location! Sorting nearby facilities...", "success");

      // Place user marker
      if (userMarker && map) map.removeLayer(userMarker);
      userMarker = L.circleMarker([userLocation.lat, userLocation.lon], {
        radius: 9,
        fillColor: '#0284C7',
        color: '#FFFFFF',
        weight: 3,
        opacity: 1,
        fillOpacity: 0.9
      }).addTo(map);
      userMarker.bindPopup("<strong>You are here</strong>").openPopup();

      map.setView([userLocation.lat, userLocation.lon], 12);

      // Re-fetch facilities with user coordinates to get distances
      const currentQuery = document.getElementById('facility-search-input')?.value.trim();
      const currentCategory = document.querySelector('.filter-cat-btn.active')?.getAttribute('data-cat') || 'ALL';
      const emergencyOnly = document.getElementById('emergency-filter-toggle')?.checked || false;

      loadFacilities({
        query: currentQuery,
        category: currentCategory,
        emergency_only: emergencyOnly,
        lat: userLocation.lat,
        lon: userLocation.lon
      });
    },
    (err) => {
      console.warn("Geolocation denied or error:", err);
      if (btn) btn.innerHTML = `<span>📍 Use My Location</span>`;
      showToast("Location access was denied or timed out. You can still search by village or pin code.", "error");
    },
    { enableHighAccuracy: true, timeout: 8000 }
  );
}

// Setup Event Listeners
function setupFacilityFilters() {
  const searchInput = document.getElementById('facility-search-input');
  if (searchInput) {
    let timeout = null;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        applyAllFilters();
      }, 350);
    });
  }

  document.querySelectorAll('.filter-cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-cat-btn').forEach(b => b.classList.remove('active', 'btn-primary'));
      document.querySelectorAll('.filter-cat-btn').forEach(b => b.classList.add('btn-outline'));
      
      btn.classList.add('active', 'btn-primary');
      btn.classList.remove('btn-outline');
      applyAllFilters();
    });
  });

  const emergToggle = document.getElementById('emergency-filter-toggle');
  if (emergToggle) {
    emergToggle.addEventListener('change', () => {
      applyAllFilters();
    });
  }

  const locBtn = document.getElementById('btn-get-location');
  if (locBtn) {
    locBtn.addEventListener('click', requestUserLocation);
  }
}

function applyAllFilters() {
  const query = document.getElementById('facility-search-input')?.value.trim();
  const category = document.querySelector('.filter-cat-btn.active')?.getAttribute('data-cat') || 'ALL';
  const emergencyOnly = document.getElementById('emergency-filter-toggle')?.checked || false;

  const params = {
    query: query,
    category: category,
    emergency_only: emergencyOnly
  };

  if (userLocation) {
    params.lat = userLocation.lat;
    params.lon = userLocation.lon;
  }

  loadFacilities(params);
}

// Initial page mount
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  setupFacilityFilters();

  // Check URL query parameters (e.g. from Triage page: ?category=HOSPITAL)
  const urlParams = new URLSearchParams(window.location.search);
  const requestedCategory = urlParams.get('category');
  if (requestedCategory) {
    const targetBtn = document.querySelector(`.filter-cat-btn[data-cat="${requestedCategory}"]`);
    if (targetBtn) {
      document.querySelectorAll('.filter-cat-btn').forEach(b => b.classList.remove('active', 'btn-primary'));
      targetBtn.classList.add('active', 'btn-primary');
      targetBtn.classList.remove('btn-outline');
    }
  }

  loadFacilities({ category: requestedCategory || 'ALL' });
});
