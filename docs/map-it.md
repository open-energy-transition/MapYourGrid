---
hide:
  - navigation
  - toc
  - footer
---

<div class="page-headers">
<h1>Map It 📍</h1>
</div>
Welcome to our interactive launchpad and hub for contributing to power grid mapping via OpenStreetMap! Click on a country or state below to start mapping power infrastructure directly in JOSM. :rocket:
If this is your first time grid mapping, please go through the [Starter-Kit](starter-kit.md). You can use the **#MapYourGrid** hashtag in your changeset to show your support for our initiative when you make an edit! To start mapping, please open [JOSM](https://josm.openstreetmap.de/), ensure that remote control is activated in `Preferences` and load your data: 

1. The **Default Transmission (90 kV+)** pulls all power infrastructure relevant for the **transmission grid**. For more details about which data is pulled via Overpass please read our [OpenStreetMap Grid Definitions](https://github.com/open-energy-transition/osm-grid-definition). Distribution grids are barely visible in satellite data and should therefore only be mapped in individual cases.
2. The Osmose, Global Energy Monitor, and Wikidata buttons provide **hint layer** data, which you can read about in our [Tools and Strategies](tools.md) page. Please note that this hint layers only work at a national level. 

<!-- Beginning of Map section-->
<style>
#map {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 600px;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid #ddd;
}

@media (max-width: 768px) {
    #map {
        height: 400px;
    }
}
</style>

<!-- Osmose button-->
<div id="osmose-panel" style="display:none; margin-bottom:1em;">
  <label for="osmoseIssue">Issue type:</label>
  <select id="osmoseIssue">
    <option value="" disabled selected>Select an Osmose Issue…</option>
    <optgroup label="Power lines (item 7040)">
                <option value="7040:1">Lone power tower or pole (Class 1)</option>
                <option value="7040:2">Unfinished power transmission line (Class 2) (recommended for beginners ⭐)</option>
                <option value="7040:3">Connection between different voltages (Class 3)</option>
                <option value="7040:4">None power node on power way (Class 4)</option>
                <option value="7040:5">Missing power tower or pole (Class 5)</option>
                <option value="7040:6">Unfinished power distribution line (Class 6)</option>
                <option value="7040:7">Unmatched voltage of line on substation (Class 7)</option>
                <option value="7040:8">Power support line management suggestion (Class 8)</option>
                <option value="7040:95">missing power=line in the area (Class 95)</option>
              </optgroup>
              <optgroup label="Power substation, ref not integrated (item 7190)">
                <option value="7190:2">Power substation is not known by the operator or misses substation=* value (Class 2)</option>
                <option value="7190:22">Power line branch not known by the operator (Class 22)</option>
              </optgroup>
              <optgroup label="Power plant (item 8270)">
                <option value="8270:1">Power plant not integrated, geocoded at municipality level (Class 1)</option>
                <option value="8270:6">Wind turbine not integrated (Class 6)</option>
              </optgroup>
              <optgroup label="Power substation (item 8280)">
                <option value="8280:1">Power substation missing in OSM or without tag "ref:FR:RTE" (Class 1)</option>
                <option value="8280:11">Minor distribution power substation missing in OSM (Class 11)</option>
                <option value="8280:21">Power line branch is missing in OSM or without tag "ref:FR:RTE" (Class 21)</option>
                <option value="8280:94">power=substation from opendata (Class 94)</option>
              </optgroup>
              <optgroup label="Power substation, could be integrated (item 8281)">
                <option value="8281:3">Power substation, integration suggestion (Class 3)</option>
                <option value="8281:13">Power minor distribution substation, integration suggestion (Class 13)</option>
                <option value="8281:23">Power line branch, integration suggestion (Class 23)</option>
                <option value="8281:94">power=substation from opendata (Class 94)</option>
              </optgroup>
              <optgroup label="Power substation, need update (item 8282)">
                <option value="8282:4">Power substation update (Class 4)</option>
                <option value="8282:24">Power line branch update (Class 24)</option>
              </optgroup>
              <optgroup label="Power support (item 8290)">
                <option value="8290:1">Power support not integrated (Class 1)</option>
                <option value="8290:2">Power support, line management suggestion (Class 2)</option>
                <option value="8290:10">Power line not integrated (Class 10)</option>
                <option value="8290:1001">Power pole not integrated (Class 1001)</option>
                <option value="8290:1004">Power pole update (Class 1004)</option>
                <option value="8290:1011">Power pole not integrated (Class 1011)</option>
              </optgroup>
    </select>
    <div class="query-version">Warning: GeoJSON file. "Open" in JOSM, but do not "upload" this layer</div>
</div>

<!-- Wikidata button-->
<div id="wikidata-panel" style="display:none; margin-bottom:1em;">
  <label for="wikidataType">Data type:</label>
  <select id="wikidataType">
    <option value="All power-related infrastructure" selected>All power-related infrastructure</option>
    <option value="substations">Substations</option>
    <option value="powerplants">Power Plants</option>
  </select>
</div>

<!-- PPM button -->
<div id="ppm-panel" style="display:none; margin-bottom:1em;">
  <label for="ppmType">Data type:</label>
  <select id="ppmType">
    <option value="Rejected power plants" selected>Rejected power plants</option>
  </select>
</div>


<div id="map"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>

<!-- SheetJS for in‑browser XLSX parsing -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>

<script>

// ———————————————
// Osmose name overrides (some names are different, check the API)
// ———————————————
const osmoseNameOverrides = {
  "Bosnia and Herzegovina": "bosnia_herzegovina",
  "eSwatini": "swaziland",
  "United States": "usa"
  // add more special cases here if needed
};


// Map
// Define world bounds (southWest & northEast corners)
const southWest = L.latLng(-90, -200);
const northEast = L.latLng( 90,  200);
const worldBounds = L.latLngBounds(southWest, northEast);

// Create the map with maxBounds & disable world wrapping
const map = L.map('map', {
  worldCopyJump: false,      // disable dragging to duplicate worlds
  minZoom: 2.2,               
  maxZoom: 18,
  maxBounds: worldBounds,    // restrict the view
  maxBoundsViscosity: 0.3    // “sticky” at the edges
}).setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors'
}).addTo(map);

// Define large countries that should use regional boundaries when zoomed in
const largeCountries = ['BR', 'US', 'CA', 'IN', 'MX', 'AU', 'CN'];
const zoomThreshold = 5; // Zoom level at which to show regions instead of countries

// Layers for countries and regions
const countriesLayer = L.geoJSON(null, {
    style: { color: '#3388ff', weight: 1 }
}).addTo(map);

const regionsLayer = L.geoJSON(null, {
    style: { color: '#3388ff', weight: 1 }
});


// Make the popup message bigger and nicer for new mappers (like Ad-blocker...)
map.options.maxPopupWidth = 300;

// 2) Dynamic query‑mode discovery via GitHub Contents API
const GITHUB_API_QUERIES =
  'https://api.github.com/repos/open-energy-transition/osm-grid-definition/contents/queries';

/** Base URL for raw file fetches (OverpassQL and version.txt) */
const RAW_BASE =
  'https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/main/queries';

let currentMode = null;

// 2a) discover all folders under /queries
async function loadModes() {
  const res = await fetch(GITHUB_API_QUERIES);
  if (!res.ok) throw new Error('Cannot load query modes from GitHub API');
  const items = await res.json();
  // keep only directory entries
  const modes = items.filter(i => i.type === 'dir').map(i => i.name);
  if (modes.length === 0) throw new Error('No query folders found');
  return modes;
}

// 2.1a) fetch the version.txt for the given mode
async function fetchVersion(mode) {
  const url = `${RAW_BASE}/${mode}/version.txt`;
  const r   = await fetch(url);
  if (!r.ok) throw new Error('version not found');
  return (await r.text()).trim();
}

// 2b) render one button per folder name
async function initQueryUI() {
  // 1. Load real modes from GitHub
  let modes = await loadModes();
  modes = modes.filter(m => m !== 'Osmose_issues');
  modes.sort((a, b) => {
    if (a === 'Default') return -1;
    if (b === 'Default') return 1;
    return a.localeCompare(b);
  });

  // inject our special modes:
  modes.splice(2, 0, 'Osmose_issues', 'GEM_powerplants', 'Wikidata', 'PPM');

  currentMode = modes.includes('Default') ? 'Default' : modes[0];

  // 2. Create two sibling containers, then insert them above the map
  const mapEl = document.getElementById('map');

  // — Row 1 title —
  const overpassTitle = document.createElement('div');
  overpassTitle.className = 'tools-header';
  overpassTitle.textContent = 'Transmission Overpass Query';
  mapEl.parentNode.insertBefore(overpassTitle, mapEl);

  const overpassContainer = document.createElement('div');
  overpassContainer.id = 'overpass-buttons';
  mapEl.parentNode.insertBefore(overpassContainer, mapEl);
  
  // — Row 2 title —
  const toolTitle = document.createElement('div');
  toolTitle.className = 'tools-header';
  toolTitle.textContent = 'Tools and Hints';
  mapEl.parentNode.insertBefore(toolTitle, mapEl);

  const toolContainer = document.createElement('div');
  toolContainer.id = 'tool-buttons';
  mapEl.parentNode.insertBefore(toolContainer, mapEl);

  // 3. Render each mode into the appropriate row
  for (const mode of modes) {
    let group;
    if (mode === 'Osmose_issues') {
      group = renderOsmoseButtonGroup();
    } else if (mode === 'GEM_powerplants') {
      group = renderGEMButtonGroup();
    } else if (mode === 'Wikidata') {
      group = renderWikidataButtonGroup();
    } 
    else if (mode === 'PPM') {
    group = renderPPMButtonGroup();
    }
    else {
      group = await renderModeButtonGroup(mode);
    }

    // Tools go in the second row, everything else in the first
    if (['Osmose_issues', 'GEM_powerplants', 'Wikidata', 'PPM'].includes(mode)) {
      toolContainer.appendChild(group);
    } else {
      overpassContainer.appendChild(group);
    }
  }

  const panelWrapper = document.createElement('div');
  panelWrapper.id = 'panel-wrapper';
  panelWrapper.style.margin = '1em 0';  // optional spacing

  // grab (and remove) the existing panels from their old position
  const osmose   = document.getElementById('osmose-panel');
  const wikidata = document.getElementById('wikidata-panel');
  const ppm      = document.getElementById('ppm-panel');

  // append them into our wrapper
  panelWrapper.appendChild(osmose);
  panelWrapper.appendChild(wikidata);
  panelWrapper.appendChild(ppm);

  // finally, drop that wrapper just before the map div
  mapEl.parentNode.insertBefore(panelWrapper, mapEl);
}

function renderOsmoseButtonGroup() {
  const btn = document.createElement('button');
  btn.textContent = 'Osmose Issues';
  btn.classList.add('query-btn');
  if (currentMode === 'Osmose_issues') btn.classList.add('active');
  btn.onclick = () => selectMode('Osmose_issues', btn);

  const ver = document.createElement('div');
  ver.classList.add('query-version');
  ver.textContent = '';  // no version

  // Osmose website link
  const info = document.createElement('div');
  info.classList.add('query-version');
  info.style.marginTop = '0.2rem';
  info.innerHTML =
   '<a href="https://osmose.openstreetmap.fr/" target="_blank">osmose.openstreetmap.fr/</a>';
   

  const group = document.createElement('div');
  group.classList.add('query-group');
  group.appendChild(btn);
  group.appendChild(ver);
  group.appendChild(info);
  return group;
}

function renderGEMButtonGroup() {
  const btn = document.createElement('button');
  btn.textContent = 'Global Energy Monitor - Power Plants';
  btn.classList.add('query-btn');
  if (currentMode === 'GEM_powerplants') btn.classList.add('active');
  btn.onclick = () => selectMode('GEM_powerplants', btn);
  
  // GEM website link + CC BY 4.0
  const info = document.createElement('div');
  info.classList.add('query-version');
  info.style.marginTop = '0.2rem';
  info.innerHTML =
   '<a href="https://globalenergymonitor.org/" target="_blank">globalenergymonitor.org</a>' +
   ' | CC BY 4.0';

  const group = document.createElement('div');
  group.classList.add('query-group');
  group.appendChild(btn);
  group.appendChild(info);
  return group;
}

function renderWikidataButtonGroup() {
  const btn = document.createElement('button');
  btn.textContent = 'Wikidata';
  btn.classList.add('query-btn');
  if (currentMode === 'Wikidata') btn.classList.add('active');
  btn.onclick = () => selectMode('Wikidata', btn);

   // Wiki repo link

  const ver = document.createElement('div');
  ver.classList.add('query-version');
  ver.textContent = ''; // no version for now

  const info = document.createElement('div');
  info.classList.add('query-version');
  info.style.marginTop = '0.2rem';
  info.innerHTML =
   '<a href="https://github.com/open-energy-transition/osm-wikidata-toolset" target="_blank">Repository</a>';

  const group = document.createElement('div');
  group.classList.add('query-group');
  group.appendChild(btn);
  group.appendChild(info);
  return group;
}

function renderPPMButtonGroup() {
  const btn = document.createElement('button');
  btn.textContent = 'powerplantmatching';
  btn.classList.add('query-btn');
  if (currentMode === 'PPM') btn.classList.add('active');
  btn.onclick = () => selectMode('PPM', btn);

  const info = document.createElement('div');
  info.classList.add('query-version');
  info.style.marginTop = '0.2rem';
  info.innerHTML =
   '<a href="https://github.com/open-energy-transition/mapit-osm/tree/main" target="_blank">Repository</a>';

  const group = document.createElement('div');
  group.classList.add('query-group');
  group.appendChild(btn);
  group.appendChild(info);
  return group;
}


async function renderModeButtonGroup(mode) {
  const btn = document.createElement('button');
  // I overrided the button name for Default, but the file in github is still Default
  if (mode === 'Default') {
  btn.textContent = 'Default Transmission (90 kV+)';
  } else {
  btn.textContent = mode.replace(/_/g, ' ');
  }
  btn.classList.add('query-btn');
  if (mode === currentMode) btn.classList.add('active');
  btn.onclick = () => selectMode(mode, btn);

  // —— make version badge into a link to the GitHub folder ——
  const verLink = document.createElement('a');
  verLink.classList.add('query-version');
  verLink.target = '_blank';
  // encode mode so "400kv+" becomes "400kv%2B"
  const repoFolderUrl =
   `https://github.com/open-energy-transition/osm-grid-definition/tree/main/queries/` +
   encodeURIComponent(mode);
  verLink.href = repoFolderUrl;  try {
    const v = await fetchVersion(mode);
    verLink.textContent = `v${v}`;
  } catch {
    verLink.textContent = 'v?';
  }

  const group = document.createElement('div');
  group.classList.add('query-group');
  group.appendChild(btn);
  group.appendChild(verLink);
  return group;
}

// helper to swap modes and show/hide the Osmose and wikidata UI panels
function selectMode(mode, btn) {
  currentMode = mode;
  document.querySelectorAll('.query-btn')
          .forEach(b => b.classList.toggle('active', b === btn));

  // Osmose
  document.getElementById('osmose-panel').style.display =
    mode === 'Osmose_issues' ? 'block' : 'none';

  // Wikidata
  document.getElementById('wikidata-panel').style.display =
    mode === 'Wikidata' ? 'block' : 'none';

  // PPM    
  document.getElementById('ppm-panel').style.display =
  mode === 'PPM' ? 'block' : 'none';
}




// 2c) fetch the correct OverpassQL file on demand
async function fetchQuery(mode, adminLevel) {
  const rawUrl =
    `https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/` +
    `main/queries/${mode}/admin${adminLevel}.overpassql`;
  const r = await fetch(rawUrl);
  if (!r.ok) throw new Error(`Query file not found: ${mode}/admin${adminLevel}`);
  return r.text();
}

// 2d) unified click handler for country (level 2) & region (level 4)
async function handleAreaClick(iso, level, layer) {
  const name = level === 2 
    ? layer.feature.properties.NAME      // Countries use NAME
    : layer.feature.properties.NAME_1;   // Regions use NAME_1
  const sovName= layer.feature.properties.SOVEREIGNT; // for linking to Osmose

  // Normalize ONLY for Wikidata
  let usedSovName = sovName;
  if (currentMode === 'Wikidata') {
    const normalizedSovNameMap = {
      "China": "People's_Republic_of_China"
      // Add more mappings as needed
    };
    usedSovName = normalizedSovNameMap[sovName] || sovName;
  }


  umami.track('map-click');
  layer.setStyle({ color: '#ff7800' });
  layer.getPopup().setContent(`Loading ${name}…`).update();

  try {
    if (currentMode === 'Osmose_issues') {
      await fetchOsmoseAndDownload(sovName);
    }
    else if (currentMode === 'GEM_powerplants') {
      await fetchGEMAndDownload(sovName);
    }
    else if (currentMode === 'Wikidata') {
      await fetchWikidataAndDownload(usedSovName);
    }
    else if (currentMode === 'PPM') {
    await fetchPPMAndDownload(sovName);
    }
    else {
       let tpl = await fetchQuery(currentMode, level);
       tpl = tpl.replace(/\$\{iso\}/g, iso);
       sendToJosm(tpl);
    }
  } catch (err) {
    layer.getPopup().setContent(`Error: ${err.message}`).update();
  }

setTimeout(() => {
  layer.setStyle({ color: '#3388ff' });

  const html = `
    <div class="popup-success">
      <p>🎉 <strong>Great!</strong> Now go back to JOSM and check if it is downloading. Depending on the country, this may take <em>60 seconds or more</em>. The grid of some countries are to large to be mapped on a national level. However, you can zoom in and click on regions or states.</p>
      <p>For <strong>tools and hints</strong> selections, you will need to download the geojson file. Afterwards drag and drop the file into JSOM.</p>
      <p>⚠️ <strong>If nothing happens:</strong></p>
      <ol>
        <li>Check if your ad-blocker is off</li>
        <li>Make sure JOSM is open</li>
        <li>Make sure Remote Control is enabled in JOSM</li>
        <li>If it’s enabled but still not working, toggle it off and on again</li>
        <li>Note that hint layers do not work on national layers. In this case, please load the data onto a national layer.</li>
      </ol>
    </div>
  `;

  layer.getPopup()
       .setContent(html)
       .update();
}, 2000);
}

// initialize the UI immediately
initQueryUI().catch(console.error);

// Osmose API fetcher
async function fetchOsmoseAndDownload(sovName) {
  const sel = document.getElementById('osmoseIssue');
  if (!sel.value) {
    alert('Please select an issue type first.');
    return;
  }
  const [item, cls] = sel.value.split(':');
  /// normalize to lowercase, add underscore for +1 words  and add wildcard
  // apply override if present, else slugify normally
  const key = osmoseNameOverrides[sovName] || sovName;
  let base = key
             .toLowerCase()
             .replace(/\s+/g, '_');
  if (!base.endsWith('*')) base += '*';

  const apiUrl = 
    `https://osmose.openstreetmap.fr/api/0.3/issues.json?` +
    `country=${encodeURIComponent(base)}` +
    `&item=${item}&class=${cls}&limit=500`;

  const resp = await fetch(apiUrl);
  if (!resp.ok) throw new Error(`Osmose API ${resp.statusText}`);
  const data = await resp.json();

  const features = (data.issues||[]).map(i => ({
    type: 'Feature',
    properties: { id: i.id, item: i.item, clazz: i.class },
    geometry: { type: 'Point', coordinates: [i.lon, i.lat] }
  }));

  // If no features, notify and stop
  if (features.length === 0) {
    alert(`No issues found for "${sel.options[sel.selectedIndex].text}" in ${sovName.replace('*','')}. Try another osmose issue type!`);
    return;
  }

  const geojson = { type: 'FeatureCollection', features };

  const blob = new Blob([JSON.stringify(geojson, null,2)],
                        {type:'application/json'});
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `${sovName.replace('*','')}_osmose_${item}_${cls}.geojson`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

async function fetchGEMAndDownload(sovName) {
  const countryKey = sovName.trim().toLowerCase();

  // 1) fetch the XLSX from your own /data/ folder
  const resp   = await fetch('/data/GEM-Global-Integrated-Power-February-2025-update-II.xlsx');
  if (!resp.ok) throw new Error(`XLSX fetch failed: ${resp.statusText}`);
  const arrayBuffer = await resp.arrayBuffer();

  // 2) parse it with SheetJS
  const wb        = XLSX.read(arrayBuffer, { type: 'array' });
  const sheetName = wb.SheetNames[1];          // second tab → index 1
  const rows      = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], { defval: '' });

  // 3) filter + map into GeoJSON Features
  const features  = rows
    .filter(r => (r['Country/area'] || '').trim().toLowerCase() === countryKey)
    .map(r => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [Number(r.Longitude), Number(r.Latitude)]
      },
      properties: Object.fromEntries(
        Object.entries(r).filter(([k]) => !['Latitude','Longitude'].includes(k))
      )
    }));

  if (features.length === 0) {
    return alert(`No GEM powerplants found for ${sovName}.`);
  }

  // 4) download as GeoJSON
  const geojson = { type: 'FeatureCollection', features };
  const blob    = new Blob([JSON.stringify(geojson, null, 2)], { type: 'application/json' });
  const url     = URL.createObjectURL(blob);
  const a       = document.createElement('a');
  a.href        = url;
  a.download    = `${sovName.replace(/\s+/g, '_')}_gem_powerplants.geojson`;
  a.click();
  URL.revokeObjectURL(url);
}

async function fetchWikidataAndDownload(sovName) {
  // grab the value of the wikidataType so "substations" or "powerplants" from the button selected (go up the script)
  const type = document.getElementById('wikidataType').value;

  // Here it fetches the folders from the github rpo:
  //   To add, put the value on the left (value is the value of the button wikidatatype), and on the right the name of the geojson folder from the github repo
   const foldertypes = {
    'All power-related infrastructure': '/output_by_qid_v2/geojson_by_country',
    'substations': '/substations/geojson_by_country',
    'powerplants': '/output_by_qid/Q159719_power_plant'
  };

  const folder = foldertypes[type];
  if (!folder) {
    return alert(`Unknown data type: ${type}`);
  }

  const fileName = sovName.replace(/\s+/g,'_') + '.geojson';
  const url = `https://raw.githubusercontent.com/open-energy-transition/osm-wikidata-toolset/main/`
            + `${folder}/${fileName}`;

  const resp = await fetch(url);
  if (!resp.ok) {
    return alert(`No Wikidata ${type.replace(/_/g,' ')} file for ${sovName}.`);
  }
  const geojson = await resp.json();

  // Trigger download
  const blob = new Blob([JSON.stringify(geojson, null,2)], {type:'application/json'});
  const a    = document.createElement('a');
  a.href     = URL.createObjectURL(blob);
  a.download = `${sovName.replace(/\s+/g,'_')}_wikidata_${type}.geojson`;
  a.click();
  URL.revokeObjectURL(a.href);
}

async function fetchPPMAndDownload(sovName) {
  const type = document.getElementById('ppmType').value;

  const foldertypes = {
    'Rejected power plants': '/ppm_rejected_geojson_by_country'
  };

  const folder = foldertypes[type];
  if (!folder) {
    return alert(`Unknown data type: ${type}`);
  }

  const fileName = sovName.replace(/\s+/g, '_') + '.geojson';
  const url = `https://raw.githubusercontent.com/open-energy-transition/mapit-osm/main${folder}/${fileName}`;

  const resp = await fetch(url);
  if (!resp.ok) {
    return alert(`No PPM file found for ${sovName}.`);
  }

  const geojson = await resp.json();
  const blob = new Blob([JSON.stringify(geojson, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${sovName.replace(/\s+/g, '_')}_ppm_${type}.geojson`;
  a.click();
  URL.revokeObjectURL(a.href);
}



// JOSM integration function
function sendToJosm(query) {
  // Encode only the query part
  const encodedQuery = encodeURIComponent(query);
  
  // Construct the Overpass URL by inserting the encoded query.
  const overpassUrl = "https://overpass-api.de/api/interpreter?data=" + encodedQuery;
  
  // Build the final JOSM URL by concatenating the strings manually.
  const josmUrl = "http://localhost:8111/import?new_layer=true&url=" + overpassUrl;

  // Keep a log to see the actual URL
  console.log("URL ", josmUrl);
  
  const iframe = document.createElement('iframe');
  iframe.style.display = 'none';
  iframe.src = josmUrl;
  document.body.appendChild(iframe);
  setTimeout(() => document.body.removeChild(iframe), 1000);
}

// Handle zoom events to show/hide the appropriate layers
map.on('zoomend', function() {
    const currentZoom = map.getZoom();
    
    if (currentZoom >= zoomThreshold) {
        // When zoomed in enough, hide countries and show regions
        if (!map.hasLayer(regionsLayer)) {
            map.addLayer(regionsLayer);
        }
    } else {
        // When zoomed out, hide regions
        if (map.hasLayer(regionsLayer)) {
            map.removeLayer(regionsLayer);
        }
    }
});

// Load country GeoJSON and add interactivity
fetch('../data/countries.geojson')
  .then(response => response.json())
  .then(countries => {
    countriesLayer.addData(countries);

    countriesLayer.eachLayer(layer => {
      const iso  = layer.feature.properties.ISO_A2;
      const name = layer.feature.properties.NAME;

      layer.bindPopup(`<b>${name}</b><br>Click to load in JOSM`);
      layer.on('click', () => {
        // large countries should be clicked at region level when zoomed in
        if (largeCountries.includes(iso) && map.getZoom() >= zoomThreshold) {
          layer
            .getPopup()
            .setContent(`<b>${name}</b><br>Please click on a specific region`)
            .update();
          return;
        }
        handleAreaClick(iso, 2, layer);
      });
    });
  })
  .catch(error => console.error('Countries GeoJSON error:', error));

// Load region GeoJSON and add interactivity
fetch('../data/regionsv2.geojson')
  .then(response => response.json())
  .then(regions => {
    regionsLayer.addData(regions);

    regionsLayer.eachLayer(layer => {
      const iso3166_2 = layer.feature.properties.ISO_1;
      const name      = layer.feature.properties.NAME;

      layer.bindPopup(`<b>${name}</b><br>Click to load in JOSM`);
      layer.on('click', () => {
        handleAreaClick(iso3166_2, 4, layer);
      });
    });
  })
  .catch(error => console.error('Regions GeoJSON error:', error));
</script>

??? info "Map Legend for the recommended [MapCSS](starter-kit.md#coloring-your-grid-map-and-legend) (Click Me)"
    <img 
      src="https://raw.githubusercontent.com/open-energy-transition/color-my-grid/refs/heads/main/legend/power-grid-legend.png" 
      class="img-border image-caption" 
      alt="Power Grid Legend"
      style="display: block; margin-left: auto; margin-right: auto;"
      width="600">

:mag: Below you can find "Starter powerlines" where we have found some lines which you can map if you are new. <br>
**Please** check the box if you mapped this line, so as to not waste other people's time! Once part of the community, we can grant you access to this spreadsheet so you can add other lines if you want.

??? success "Starter powerlines (Click Me)"
    <iframe
     src="https://docs.google.com/spreadsheets/d/13YZftK9xZ09t2oSvhwjE0Zb7P25nl9OaUAxIBVNH0js/edit?usp=sharing&rm=minimal"
     class="iframestyle"
     style="width:100%; height: 500px; border:1px solid #ddd; ">
    </iframe>
<!-- I couldn't make the page not go "up" when using this iframe, so for now there is this chatgpt js script that prevents this. It was very annoying, but if you have a better solution that would be great-->

??? success "Curated Electrical Grid Maps (Click Me)"
    <div class="no-toc">
    --8<-- "docs/awesome.md"
    </div>

<script>
  let lastScrollY = window.scrollY;
  // Select your iframe by its class or ID. Make sure 'iframestyle' is unique enough
  // If you have multiple iframes with 'iframestyle', you might need a more specific selector
  // e.g., document.querySelector('.iframestyle[src*="google.com/spreadsheets"]')
  const iframe = document.querySelector('.iframestyle'); 

  if (iframe) { // Check if the iframe element exists
    // Add a listener to the window for scroll events
    window.addEventListener('scroll', () => {
      // Check if the scroll difference is significant, suggesting an iframe-triggered jump
      const scrollDiff = Math.abs(window.scrollY - lastScrollY);

      // You might need to adjust this threshold (e.g., 100, 150, 250, etc.)
      // A large scroll difference is likely an automatic scroll, not a user scroll
      if (scrollDiff > 100 && document.activeElement === iframe) {
        // If the iframe is currently focused and a large scroll occurred,
        // revert the scroll position to where it was before the jump
        window.scrollTo(0, lastScrollY);
      } else {
        // Otherwise, update the last scroll position
        lastScrollY = window.scrollY;
      }
    });

    // Ensure lastScrollY is correctly set when the iframe loads
    iframe.addEventListener('load', () => {
      lastScrollY = window.scrollY; // Reset lastScrollY after iframe loads
    });

    // Also update lastScrollY on mouseleave from iframe (user scrolled away from iframe)
    iframe.addEventListener('mouseleave', () => {
      lastScrollY = window.scrollY;
    });

    // And on mousedown (when user clicks inside the iframe)
    iframe.addEventListener('mousedown', () => {
        lastScrollY = window.scrollY;
    });

  } else {
    console.warn("Google Sheets iframe not found for scroll-prevention script.");
  }
</script>

## <div class="tools-header">Mapping Guidelines and Code of Mappers</div>
The following list provides the main good practices for mapping different power infrastructure in OpenStreetMap:

* [Power networks](https://wiki.openstreetmap.org/wiki/Power_networks)
* [Power networks/Guidelines](https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines)
* [Power networks/Guidelines/Power lines](https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Power_lines)
* [Power networks/Guidelines/Substations](https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Substations)
* [Power generation/Guidelines/Hydropower](https://wiki.openstreetmap.org/wiki/Power_generation/Guidelines/Hydropower)
* [Power generation/Guidelines/Solar plants](https://wiki.openstreetmap.org/wiki/Power_generation/Guidelines/Solar_plants)
* [Power networks/Guidelines/Interconnector](https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Interconnector)

!!! note "Code of Mappers"
    **⚠️ By following our [Code of Mappers](./code-of-mappers.md), we collectively protect the integrity of the OpenStreetMap platform, foster trust with communities, and unlock the power of open data for a more resilient and just energy future. Please do NOT copy any data from hint layer directly into your OpenStreetMap data layer. Every data point in your OpenStreetMap data layer must be manually set and [verified](https://wiki.openstreetmap.org/wiki/Verifiability). The metadata must also be verified against compatible licensed sources or by people on the ground. If you cannot verify the data using satellite images or any other compatible source, please do not add this information from hint layers. This may seem like a high burden at first, but it ensures the high quality of OpenStreetMap. Before you start mapping, please find out about the mapping restrictions in the respective country. In some countries, the mapping of transmission lines is not permitted. Get in touch with local users by finding out about [local projects](https://wiki.openstreetmap.org/wiki/Power_networks). ⚠️**


## Join the Chat <img src="/icons/discord.svg" alt="Discord" class="social-icon" style="width:1.2em; vertical-align:middle; margin-left:0.5ch;"> {.tools-header style="font-weight:700"}
We welcome everyone to join our [community chat](https://discord.gg/a5znpdFWfD) called _📍-MapYourGrid_ on the PyPSA-Earth discord channel. Here you can ask questions, and interact with the community. For mapping specific questions and to participate in our free personalized training, please join our [📍-MapYourGrid-support-and-training](https://discord.gg/fBw7ARTUeR) channel. 

## <div class="tools-header">Join the Community  :calendar: </div>
We welcome everyone to join our community calls and tutorials, to learn more about the mapping process and the initiative.
<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Europe%2FBerlin&showPrint=0&title=Community%20live%20sessions&src=Y182ODE3NjE1MGIzMjY4MGRkZmUzMGM1ZTE1MDU0YTc5MTVhMzY2NmY1OGY5NjkxOGVjOTZhNDJjZWQwODQ2ZGVmQGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20&color=%23AD1457" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>
