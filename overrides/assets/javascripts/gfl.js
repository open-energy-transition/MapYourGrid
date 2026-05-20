// ── Config ──────────────────────────────────────────────────────────────────
const SUPABASE_URL      = 'https://momhpgtitabhlpsxcqxh.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vbWhwZ3RpdGFiaGxwc3hjcXhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3MzUxODMsImV4cCI6MjA3NTMxMTE4M30.IUj10ikNkwip_iZsGxR8vUWNgRtK9aaiTovpTeKvm4c';
const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// ── Utilities ────────────────────────────────────────────────────────────────
/** Escape HTML entities — prevents XSS when injecting user data into innerHTML. */
const esc = s => String(s ?? '').replace(/[&<>"']/g, c =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const idEditorUrl = (lat, lon) => `https://www.openstreetmap.org/edit#map=18/${lat}/${lon}&hashtags=mapyourgrid`;

// Fallback for rows inserted before iso2 column existed (English names only).
const NAME_TO_ISO2 = {
  'spain':'ES','france':'FR','germany':'DE','italy':'IT','portugal':'PT',
  'united kingdom':'GB','uk':'GB','great britain':'GB','england':'GB','scotland':'GB','wales':'GB','northern ireland':'GB','ireland':'IE',
  'netherlands':'NL','holland':'NL','belgium':'BE','switzerland':'CH','austria':'AT','poland':'PL',
  'czech republic':'CZ','czechia':'CZ','slovakia':'SK','hungary':'HU','romania':'RO','bulgaria':'BG',
  'greece':'GR','croatia':'HR','serbia':'RS','slovenia':'SI','bosnia and herzegovina':'BA','bosnia':'BA',
  'montenegro':'ME','albania':'AL','north macedonia':'MK','macedonia':'MK','kosovo':'XK',
  'sweden':'SE','norway':'NO','denmark':'DK','finland':'FI','iceland':'IS',
  'estonia':'EE','latvia':'LV','lithuania':'LT','ukraine':'UA','belarus':'BY','moldova':'MD','russia':'RU',
  'turkey':'TR','cyprus':'CY','malta':'MT','luxembourg':'LU','liechtenstein':'LI','monaco':'MC','andorra':'AD',
  'san marino':'SM','vatican city':'VA','vatican':'VA',
  'usa':'US','united states':'US','america':'US','us':'US','canada':'CA','mexico':'MX',
  'brazil':'BR','argentina':'AR','chile':'CL','colombia':'CO','peru':'PE','venezuela':'VE',
  'ecuador':'EC','bolivia':'BO','paraguay':'PY','uruguay':'UY','costa rica':'CR','panama':'PA',
  'guatemala':'GT','honduras':'HN','el salvador':'SV','nicaragua':'NI','belize':'BZ',
  'cuba':'CU','jamaica':'JM','haiti':'HT','dominican republic':'DO','puerto rico':'PR',
  'trinidad and tobago':'TT','bahamas':'BS','barbados':'BB','guyana':'GY','suriname':'SR',
  'china':'CN','japan':'JP','south korea':'KR','korea':'KR','north korea':'KP',
  'india':'IN','pakistan':'PK','bangladesh':'BD','sri lanka':'LK','nepal':'NP','bhutan':'BT',
  'afghanistan':'AF','iran':'IR','iraq':'IQ','saudi arabia':'SA','yemen':'YE','oman':'OM',
  'uae':'AE','united arab emirates':'AE','qatar':'QA','kuwait':'KW','bahrain':'BH','jordan':'JO',
  'lebanon':'LB','syria':'SY','israel':'IL','palestine':'PS',
  'thailand':'TH','vietnam':'VN','myanmar':'MM','burma':'MM','cambodia':'KH','laos':'LA',
  'malaysia':'MY','singapore':'SG','indonesia':'ID','philippines':'PH','brunei':'BN',
  'mongolia':'MN','kazakhstan':'KZ','uzbekistan':'UZ','turkmenistan':'TM','kyrgyzstan':'KG',
  'tajikistan':'TJ','armenia':'AM','azerbaijan':'AZ','georgia':'GE',
  'south africa':'ZA','egypt':'EG','morocco':'MA','algeria':'DZ','tunisia':'TN','libya':'LY',
  'sudan':'SD','south sudan':'SS','ethiopia':'ET','kenya':'KE','tanzania':'TZ','uganda':'UG',
  'rwanda':'RW','burundi':'BI','somalia':'SO','nigeria':'NG','ghana':'GH','ivory coast':'CI',
  "cote d'ivoire":'CI','senegal':'SN','mali':'ML','niger':'NE','burkina faso':'BF',
  'guinea':'GN','sierra leone':'SL','liberia':'LR','benin':'BJ','togo':'TG','cameroon':'CM',
  'chad':'TD','central african republic':'CF','congo':'CG','dr congo':'CD','democratic republic of congo':'CD',
  'gabon':'GA','equatorial guinea':'GQ','angola':'AO','zambia':'ZM','zimbabwe':'ZW',
  'mozambique':'MZ','malawi':'MW','madagascar':'MG','botswana':'BW','namibia':'NA',
  'lesotho':'LS','eswatini':'SZ','swaziland':'SZ','mauritius':'MU','seychelles':'SC',
  'australia':'AU','new zealand':'NZ','papua new guinea':'PG','fiji':'FJ',
};

/** Returns the flag CDN URL, preferring the stored iso2, falling back to name lookup. */
function flagUrl(line) {
  const code = line.iso2 || NAME_TO_ISO2[(line.country || '').toLowerCase()];
  return `https://flagcdn.com/24x18/${(code || 'un').toLowerCase()}.png`;
}

// ── Country resolution ───────────────────────────────────────────────────────
/**
 * Resolves any-language country name to { iso2, nameEn } via REST Countries.
 * Returns null if not found or network fails.
 */
async function resolveCountry(name) {
  try {
    const res = await fetch(
      `https://restcountries.com/v3.1/name/${encodeURIComponent(name)}?fields=name,cca2`
    );
    if (!res.ok) return null;
    const data  = await res.json();
    const first = Array.isArray(data) ? data[0] : null;
    return first ? { iso2: first.cca2, nameEn: first.name.common } : null;
  } catch {
    return null;
  }
}

// ── JOSM ─────────────────────────────────────────────────────────────────────
function openInJOSM(lat, lon) {
  const b = 0.001;
  const frame = Object.assign(document.createElement('iframe'), {
    style: 'display:none',
    src: `http://localhost:8111/zoom?left=${lon-b}&right=${lon+b}&top=${lat+b}&bottom=${lat-b}&changeset_tags=hashtags=mapyourgrid`
  });
  document.body.appendChild(frame);
  setTimeout(() => frame.remove(), 1000);
  alert('✓ Go to Map It! and load the country or region you are mapping.');
}

// ── Card template ─────────────────────────────────────────────────────────────
function buildCard(line) {
  const lat = parseFloat(line.lat ?? line.coordinates?.split(',')[0]);
  const lon = parseFloat(line.lon ?? line.coordinates?.split(',')[1]);
  if (!isFinite(lat) || !isFinite(lon)) return '';

  const id = esc(line.id);
  return `
    <div class="country-card gfl-card" data-id="${id}" data-lat="${lat}" data-lon="${lon}">
      <div class="gfl-header" onclick="toggleDropdown('${id}')">
        <img src="${flagUrl(line)}" alt="${esc(line.country)}" class="country-flag off-glb">
        <h3>${esc(line.country)}</h3>
        <div class="coordinates">${esc(line.coordinates)}</div>
        ${line.status === 'attempted' ? '<span class="attempted-badge">Attempted</span>' : ''}
        <span class="dropdown-arrow">▼</span>
      </div>
      <div id="dropdown-${id}" class="gfl-dropdown">
        ${line.details ? `<p class="details"><strong>Details: </strong>${esc(line.details)}</p>` : ''}
        <div class="editor-buttons">
          <button class="editor-btn josm-btn" data-action="josm" title="Open in JOSM">
            <img src="/images/josm_logo.jpg" alt="JOSM" class="editor-logo off-glb">
            JOSM
          </button>
          <a href="${idEditorUrl(lat, lon)}" target="_blank" rel="noopener" class="editor-btn id-btn">
            <img src="/images/starter-kit/osm-logo.svg" alt="iD" class="editor-logo off-glb">
            iD Editor
          </a>
        </div>
        <div class="status-buttons">
          <label class="checkbox-label">
            <input type="checkbox" data-action="attempted" data-id="${id}"
              ${line.status === 'attempted' ? 'checked' : ''}>
            Attempted mapping
          </label>
          <button class="complete-btn" data-action="complete" data-id="${id}">
            ✓ I've continued the line.
          </button>
        </div>
      </div>
    </div>`;
}

// ── Render ────────────────────────────────────────────────────────────────────
async function loadLines() {
  const container = document.getElementById('gfl-container');
  container.innerHTML = '<div id="loading">Loading good first lines...</div>';

  const { data, error } = await db.from('lines')
    .select('*')
    .neq('status', 'completed')
    .order('created_at', { ascending: true });

  if (error) {
    container.innerHTML = '<p class="error">Error loading lines. Please try again later.</p>';
    return;
  }

  container.innerHTML = data.length
    ? `<div class="gfl-grid">${data.map(buildCard).join('')}</div>`
    : '<p>No good first lines available at the moment. Add one below!</p>';
}

// ── Status updates ────────────────────────────────────────────────────────────
async function setStatus(id, status) {
  const { error } = await db.from('lines').update({ status }).eq('id', id);
  if (error) throw error;
}

async function handleComplete(id, card) {
  if (!confirm('Mark this line as completed? It will be archived and removed from the active list.')) return;
  try {
    await setStatus(id, 'completed');
    card.style.cssText = 'opacity:0;transition:opacity 0.3s';
    setTimeout(() => {
      card.remove();
      const container = document.getElementById('gfl-container');
      if (!container.querySelector('.gfl-card'))
        container.innerHTML = '<p>No good first lines available at the moment. Add one below!</p>';
    }, 300);
  } catch {
    alert('Error marking line as completed. Please try again.');
  }
}

// ── Event delegation (single listener on the container) ───────────────────────
function handleContainerClick(e) {
  const el   = e.target.closest('[data-action]');
  if (!el) return;
  const card = el.closest('.gfl-card');
  const { action } = el.dataset;

  if (action === 'josm') {
    openInJOSM(parseFloat(card.dataset.lat), parseFloat(card.dataset.lon));
  } else if (action === 'complete') {
    handleComplete(el.dataset.id, card);
  }
}

function handleContainerChange(e) {
  const inp = e.target.closest('[data-action="attempted"]');
  if (!inp) return;

  const newStatus = inp.checked ? 'attempted' : 'available';
  setStatus(inp.dataset.id, newStatus).catch(() => {
    alert('Error updating status.');
    inp.checked = !inp.checked; // revert on failure
  });

  const card  = inp.closest('.gfl-card');
  const badge = card.querySelector('.attempted-badge');
  if (inp.checked && !badge)
    card.querySelector('.dropdown-arrow').insertAdjacentHTML('beforebegin', '<span class="attempted-badge">Attempted</span>');
  else if (!inp.checked && badge)
    badge.remove();
}

// ── Dropdown toggle (called from inline onclick on the header) ────────────────
function toggleDropdown(id) {
  const dropdown = document.getElementById(`dropdown-${id}`);
  const arrow    = document.querySelector(`.gfl-card[data-id="${id}"] .dropdown-arrow`);
  const isOpen   = dropdown.style.display === 'block';
  dropdown.style.display = isOpen ? 'none' : 'block';
  if (arrow) arrow.textContent = isOpen ? '▼' : '▲';
}

// ── Form submission ───────────────────────────────────────────────────────────
const COORD_RE = /^-?\d+\.?\d*\s*,\s*-?\d+\.?\d*$/;

async function handleSubmit() {
  const coordInput = document.getElementById('add-coordinates');
  const countryInput = document.getElementById('add-country');
  const detailsInput = document.getElementById('add-details');
  const msg          = document.getElementById('form-message');
  const btn          = document.getElementById('submit-gfl');

  const coordinates = coordInput.value.trim();
  const country     = countryInput.value.trim();
  const details     = detailsInput.value.trim();

  if (!coordinates || !country) {
    msg.innerHTML = '<span class="error">Please fill in all required fields.</span>';
    return;
  }
  if (!COORD_RE.test(coordinates)) {
    msg.innerHTML = '<span class="error">Invalid coordinates. Use: lat,lon (e.g. 43.224,12.828)</span>';
    return;
  }
  const [lat, lon] = coordinates.split(',').map(Number);
  if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
    msg.innerHTML = '<span class="error">Coordinates out of range.</span>';
    return;
  }

  btn.disabled  = true;
  msg.innerHTML = '<span>Resolving country…</span>';

  try {
    const resolved = await resolveCountry(country);
    if (!resolved) {
      msg.innerHTML = `<span class="error">Country "${esc(country)}" not found. Check spelling or try the English name.</span>`;
      return;
    }

    const { error } = await db.from('lines').insert([{
      coordinates,
      country,
      country_en: resolved.nameEn,
      iso2:       resolved.iso2,
      details:    details || null,
      status:     'available',
      lat, lon,
    }]);
    if (error) throw error;

    msg.innerHTML = '<span class="success">Good first line added successfully!</span>';
    coordInput.value = countryInput.value = detailsInput.value = '';
    setTimeout(() => { msg.innerHTML = ''; loadLines(); }, 2000);
  } catch (err) {
    msg.innerHTML = `<span class="error">Error: ${esc(err.message)}</span>`;
  } finally {
    btn.disabled = false;
  }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  loadLines();

  const container = document.getElementById('gfl-container');
  container.addEventListener('click',  handleContainerClick);
  container.addEventListener('change', handleContainerChange);

  document.getElementById('submit-gfl').addEventListener('click', handleSubmit);
});
