---
hide:
  - navigation
  - toc
  - footer
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />

<div id="mapit-root">

  <!-- Left sidebar -->
  <aside id="mapit-sidebar">
    <div id="sidebar-inner">
      <a href="/" id="back-btn">← MapYourGrid</a>
      <!-- Editor (josm/id) toggle -->
      <div class="mi-section">
        <div class="mi-section-header static">Editeur</div>
        <div class="mi-section-body">
          <div class="mi-editor-switch">
            <button class="mi-switch-opt active" data-editor="josm">JOSM</button>
            <button class="mi-switch-opt"        data-editor="id">iD</button>
          </div>
          <div id="id-editor-warning" class="mi-warning hidden">
            Seulement les "Outils" marchent avec l'editeur iD 
          </div>
        </div>
      </div>
      <!-- Overpass query buttons -->
      <div class="mi-section" id="section-overpass">
        <div class="mi-section-header static">Télecharger les données</div>
        <div class="mi-section-body" id="overpass-buttons"></div>
      </div>
      <!-- iD URL box when link appears -->
      <div class="mi-section" id="id-url-section" style="display:none;">
        <div class="mi-section-body" id="id-url-container">
          <span class="mi-label">Copier pour iD → Données cartographiques → Données de carte personnalisées:</span>
          <div class="mi-url-row">
            <input type="text" id="url-display" readonly>
            <button id="copy-btn">Copier</button>
          </div>
        </div>
      </div>
      <!-- Tools & Hints (collapsible) -->
      <div class="mi-section collapsed" id="section-hints">
        <button class="mi-section-header toggle" onclick="toggleSection(this)">
          <span>Outils</span>
          <span class="mi-chevron">&#9660;</span>
        </button>
        <div class="mi-section-body">
          <div id="tool-buttons"></div>
          <div id="osmose-panel" class="mi-hint-panel hidden">
            <label for="osmoseIssue">Issue type:</label>
            <select id="osmoseIssue">
              <optgroup label="Power lines (item 7040)">
                <option value="7040:1">Lone power tower or pole (Class 1)</option>
                <option value="7040:2" selected>Unfinished transmission line (Class 2) &#11088;</option>
                <option value="7040:3">Connection between different voltages (Class 3)</option>
                <option value="7040:4">None power node on power way (Class 4)</option>
                <option value="7040:5">Missing power tower or pole (Class 5)</option>
                <option value="7040:6">Unfinished distribution line (Class 6)</option>
                <option value="7040:7">Unmatched voltage on substation (Class 7)</option>
                <option value="7040:8">Power support line management (Class 8)</option>
                <option value="7040:95">Missing power=line in area (Class 95)</option>
              </optgroup>
            </select>
            <div class="mi-meta-link">Attention: certains pays ne fonctionnent que à l'échelle nationale.</div>
          </div>
          <div id="wikidata-panel" class="mi-hint-panel hidden">
            <label for="wikidataType">Type de données:</label>
            <select id="wikidataType">
              <option value="All power-related infrastructure" selected>Tout</option>
              <option value="substations">Postes</option>
              <option value="powerplants">Centrales electriques</option>
            </select>
            <div class="mi-meta-link">Seulement à l'échelle nationale.</div>
          </div>
          <div id="ppm-panel" class="mi-hint-panel hidden">
            <label for="ppmType">Tipo de datos:</label>
            <select id="ppmType">
              <option value="Rejected power plants" selected>Centrales rechazadas</option>
            </select>
            <div class="mi-meta-link">Seulement à l'échelle nationale.</div>
          </div>
          <div id="gem-panel"   class="mi-hint-panel hidden"><div class="mi-meta-link">Seulement à l'échelle nationale.</div></div>
          <div id="solar-panel" class="mi-hint-panel hidden"><div class="mi-meta-link">Seulement à l'échelle nationale.</div></div>
          <div id="wind-panel"  class="mi-hint-panel hidden"><div class="mi-meta-link">Seulement à l'échelle nationale.</div></div>
        </div>
      </div>
      <!-- Good First Lines -->
      <div class="mi-section collapsed">
        <button class="mi-section-header toggle" onclick="toggleSection(this)">
          <span>Bonnes premieres lignes</span>
          <span class="mi-chevron">&#9660;</span>
        </button>
        <div class="mi-section-body">
          <p class="mi-body-text">Lignes que nous avons trouvées! (🔶 pays)</p>
          <a href="/good-first-lines/" class="mi-link-btn">Voir  Bonnes Premieres Lignes &#8594;</a>
        </div>
      </div>
      <!-- Map Legend -->
      <div class="mi-section">
        <button class="mi-icon-btn" onclick="openOverlay('legend')">
          <span class="mi-btn-label">&#128506;&#160; JOSM MapCSS Legende</span>
        </button>
      </div>
      <!-- JOSM Hotkeys -->
      <div class="mi-section">
        <button class="mi-icon-btn" onclick="openOverlay('hotkeys')">
          <img src="/images/josm_logo.jpg" alt="" class="mi-btn-icon off-glb">
          <span class="mi-btn-label">JOSM Raccourcis de clavier</span>
        </button>
      </div>
      <!-- Mapping Guidelines -->
      <div class="mi-section">
        <button class="mi-icon-btn" onclick="openOverlay('guidelines')">
          <span class="mi-btn-label">&#128214;&#160; Principes pour cartographier</span>
        </button>
      </div>
      <!-- Good Practices -->
      <div class="mi-section">
        <button class="mi-icon-btn" onclick="openOverlay('practices')">
          <span class="mi-btn-label">&#9888;&#160; Bonnes Pratiques</span>
        </button>
      </div>
      <!-- Community / Social -->
      <div class="mi-section collapsed">
        <button class="mi-section-header toggle" onclick="toggleSection(this)">
          <span>Communauté</span>
          <span class="mi-chevron">&#9660;</span>
        </button>
        <div class="mi-section-body">
          <a href="https://discord.gg/a5znpdFWfD" target="_blank" class="mi-link-btn">
            <img src="/icons/discord.svg" alt="" style="width:15px;height:15px;vertical-align:middle;margin-right:7px;">
            Discord →
          </a>
          <a href="https://bsky.app/profile/mapyourgrid.bsky.social" target="_blank" class="mi-link-btn">
            <span style="margin-right:7px;font-size:14px;">🦋</span>Bluesky →
          </a>
          <button class="mi-link-btn" onclick="openOverlay('calendar')">&#128197;&#160; Calendrier communautaire</button>
        </div>
      </div>

    </div>
  </aside>

  <!-- Mobile toggle -->
  <button id="mobile-menu-btn" onclick="toggleMobileSidebar()" title="Open controls">&#9776;</button>

  <!-- MAP -->
  <div id="map"></div>

  <!-- Introduction/how to use info card -->
  <div id="info-card">
    <div id="info-card-header">
      <span id="info-title">Introduction</span>
      <div id="info-nav">
        <button id="info-prev" onclick="infoCardPrev()" disabled>&#9664;</button>
        <span   id="info-pager">1 / 2</span>
        <button id="info-next" onclick="infoCardNext()">&#9654;</button>
      </div>
      <button id="info-toggle" onclick="toggleInfoCard()">&#9650;</button>
    </div>
    <div id="info-card-body"></div>
  </div>

  <!-- Country panel when a place is clicked -->
  <div id="country-panel">
    <div id="country-panel-header">
      <div id="country-panel-flag-name">
        <img id="country-flag" class="off-glb" src="" alt="">
        <span id="country-name"></span>
      </div>
      <button id="country-panel-close" onclick="hideCountryPanel()">&#10005;</button>
    </div>
    <div id="country-panel-body"></div>
  </div>

  <!-- Overlay divs for legend/josm hotkeys etc... -->
  <div id="mapit-overlay" class="hidden" onclick="closeOverlay(event)">
    <div id="overlay-content">
      <div id="overlay-content-header">
        <h3 id="overlay-title"></h3>
        <button id="overlay-close" onclick="closeOverlay()">&#10005;</button>
      </div>
      <div id="overlay-body"></div>
      <div id="overlay-slide-nav" class="hidden">
        <button onclick="overlayPrev()">&#9664; Prev</button>
        <span   id="overlay-pager"></span>
        <button onclick="overlayNext()">Next &#9654;</button>
      </div>
    </div>
  </div>

</div>

<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>

<script>
"use strict";


// CONSTANTS

// OSM grid definition repo for overpass scripts
const GITHUB_API_QUERIES =
  "https://api.github.com/repos/open-energy-transition/osm-grid-definition/contents/queries";
const RAW_BASE =
  "https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/main/queries";

// Zoom level at which region boundaries replace country boundaries.
const ZOOM_REGION_THRESHOLD = 5;

// Names that differ between the countries/regions GeoJSON and the hint layers.
const OVERRIDES = {
  osmoseCountries: {
    "Bosnia and Herzegovina":           "bosnia_herzegovina",
    "eSwatini":                         "swaziland",
    "Republic of the Congo":            "congo_brazzaville",
    "Democratic Republic of the Congo": "congo_kinshasa",
    "United States":                    "usa"
  },
  osmoseRegions: {
    "Centre-ValdeLoire": "centre",
    "MatoGrossodoSul":   "mato_grosso_do_sul",
    "MinasGerais":       "minas_gerais",
    "Cataluna":          "catalunya",
    "NeiMongol":         "inner_mongolia"
  },
  wikidata:     { "China": "People's_Republic_of_China" },
  MapYourSolar: { "Ivory Coast": "Cote_d'Ivoire" }
};

// for the names that are in the countries geojson: write in lowercase
// You can add more name mappings here if people add countries in a specific name like "DRC"
const GFL_NAME_NORMALISE = {
  "drc": "democratic republic of the congo",
};


// Text content for the bottom-left introduction info card carousel.
const INFO_SLIDES = [
  {
    title: "Introduction",
    content: "<p>Bienvenue sur notre plateforme interactive permettant de cartographier le réseau électrique via <strong>OpenStreetMap</strong>!</p><p>Sur ton ordinateur, clique sur un pays ou agrandis la carte et clique sur une région pour charger les données du réseau dans <strong>JOSM</strong> ou <strong>iD</strong>.</p><p>Vous débutez dans la cartographie du réseau électrique? Commencez avec les <a href='/starter-kit/' target='_blank'>Tutos</a>. Utilise notre hashtag <strong>#MapYourGrid</strong>!</p>"
  },
  {
    title: "Comment télécharger les données?",
    content: "<ol><li>Sélectionnez votre éditeur (JOSM ou iD) dans le panneau.</li><li>Si JOSM, ouvre <a href='https://josm.openstreetmap.de/' target='_blank'>JOSM</a> et active <em>Controle à Distance</em> dans Préferences. Assure-toi que ton bloqueur de publicités est désactivé.</li><li>Si oui, sélectionne un ensemble d'outils, puis clique sur un pays/une région.</li><li>Choisis un type de <strong>Overpass Query</strong> (dans 'Télécharger les données).</li><li>Cliquez sur un pays — ou zoomez et cliquez sur une région.</li><li>Utilise les<strong>Outils</strong> pour plus de couches de données.</li><li>Les pays en orange disposent déjà d'une 'bonne première ligne' que tu peux cartographier !</li></ol>"
  }
];

// Two-page content for the "Good Practices" modal overlay.
const PRACTICES_SLIDES = [
  {
    title: "Communautés locales et bonnes pratiques'",
    content: `<p>Avant de commencer à cartographier, renseigne-toi sur les restrictions en vigueur dans le pays concerné. Dans certains pays, il est interdit de cartographier les lignes électriques. Contacte les utilisateurs locaux en recherchant ta <a href='https://community.osm.be/' target='_blank'>communité locale OSM</a> et <a href='https://wiki.openstreetmap.org/wiki/Power_networks#Local_projects' target='_blank'>projets locaux</a>. Si tu ne trouves pas de communauté locale, merci de <a href='mailto:MapYourGrid@openenergytransition.org'>nous envoyer un courriel</a> et nous vous aideront.</p>
    <p>En suivant nos <a href='/mapping-good-practices/' target='_blank'>Good practices for mapping</a> (en anglais), nous préservons l'intégrité de la plateforme OpenStreetMap, nous renforçons la confiance au sein des communautés et nous exploitons le potentiel des données ouvertes pour bâtir un avenir énergétique plus résilient et plus juste.</p><p> <strong>Veuillez NE PAS copier les données des couches de suggestions directement dans votre couche de données OpenStreetMap.</strong> </p><p> Chaque donnée doit être saisie et vérifiée manuellement. Les métadonnées doivent également être vérifiées en les comparant à des sources fiables et compatibles, ou par des personnes sur le terrain. Si vous ne pouvez pas vérifier les données à l'aide d'images satellites ou de toute autre source fiable, n'ajoutez pas ces informations à partir des couches de suggestions. Même si cela peut sembler fastidieux au premier abord, cela garantit la haute qualité d'OpenStreetMap.</p>`
  },
  {
    title: "Risque d'un double mapping",
    content: `<p>Note que tu n'as téléchargé que les données du réseau de transport du pays, de l'État ou de la province que tu as sélectionné. Cela comprend les centrales électriques, les générateurs, les sous-stations, les pylônes à haute tension et les lignes de transport. Les autres éléments d'OpenStreetMap, comme les rues, ne seront pas visibles. Par conséquent, <strong>N'utilisez jamais nos outils pour cartographier des objets qui ne sont pas chargés via notre Overpass</strong>, sinon, les autres collaborateurs devront supprimer les données en double.</p>
    <p>Certaines lignes de transport d'électricité transfrontalières resteront visibles au-delà des limites administratives indiquées en rose. Cependant, pour les modifier, tu devras charger les deux pays. <strong>Ne trace jamais la carte au-delà des limites administratives indiquées en rose</strong>, car cela risquerait fort d'entraîner un double tracé de l'infrastructure.</p>`
  }
];

// Default state
const STATE = {
  editor:           "josm",  // "josm" | "id"
  mode:             null,    // active overpass/tool mode string
  regionsLoaded:    false,
  infoSlide:        0,
  infoCollapsed:    false,
  overlaySlides:    null,    // PRACTICES_SLIDES or null for single-page overlays
  overlaySlideIdx:  0,
  versionCache:     {},      // mode → version string, to avoid duplicate fetches
  lowVoltageForced: false    // when true, 220 kV lines stay visible at every zoom
};

// Built from GeoJSON at load time: ISO A2 → country display name.
// Used to find the parent country name when a region is clicked.
const countryNameMap = {};

// Lowercase country names that have at least one active Good First Line entry.
// Populated by fetchGFLCountries() before country layers are styled.
let GFL_COUNTRY_NAMES = new Set();


// Map loading

// maxBounds restricts panning to exactly one world map.
// maxBoundsViscosity: 1.0 = completely rigid boundary, no elastic scrolling past it.
const map = L.map("map", {
  minZoom:              3,
  maxZoom:              18,
  maxBounds:            [[-80, -230], [85, 195]],
  maxBoundsViscosity:   1.0,
  worldCopyJump:        false,
  zoomControl: false // this disables the zoom buttons on the left side
}).setView([20, 0], 2);

// Tile layer chosen here, and zoom
L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}", {
  attribution: "Tiles &copy; <a href='https://www.esri.com' target='_blank'>Esri</a>, USGS, NOAA | © <a href='https://www.openstreetmap.org/copyright' target='_blank'>OpenStreetMap</a> contributors",
  maxZoom: 19,
  noWrap:  true // noWrap: true stops the tile layer from repeating tiles outside [-180, 180].
}).addTo(map);

// Zoom buttons top right
L.control.zoom({ position: "topright" }).addTo(map);

// Fullscreen button 
L.Control.Fullscreen = L.Control.extend({
  onAdd() {
    const btn = L.DomUtil.create("button", "leaflet-bar leaflet-control");
    btn.innerHTML = "&#x26F6;";
    btn.title = "Toggle fullscreen";
    btn.style.cssText = "width:30px;height:30px;cursor:pointer;font-size:14px;line-height:28px;background:white;border:none;";
    L.DomEvent.disableClickPropagation(btn);
    L.DomEvent.on(btn, "click", () =>
      document.fullscreenElement ? document.exitFullscreen() : map.getContainer().requestFullscreen()
    );
    return btn;
  },
  onRemove() {}
});
new L.Control.Fullscreen({ position: "topright" }).addTo(map);

// 220 kV toggle button. Default is OFF
// When Off: 220 kV lines only show past ZOOM_REGION_THRESHOLD (currently 5).
// When ON: 220 kV lines load and stay visible at every zoom level.
L.Control.LowVoltageToggle = L.Control.extend({
  onAdd() {
    const btn = L.DomUtil.create("button", "leaflet-bar leaflet-control mi-lowv-btn");
    btn.innerHTML = "220";
    btn.title = "Montrer les lignes 220+ kV";
    btn.style.cssText = "width:30px;height:30px;cursor:pointer;font-size:10px;font-weight:700;line-height:28px;background:white;color:#333;border:none;text-align:center;";

    L.DomEvent.disableClickPropagation(btn);
    L.DomEvent.on(btn, "click", () => {
      STATE.lowVoltageForced = !STATE.lowVoltageForced;
      btn.style.background = STATE.lowVoltageForced ? "#c73030" : "white";
      btn.style.color      = STATE.lowVoltageForced ? "#fff"    : "#333";
      if (STATE.lowVoltageForced) {
        showPowerLinesLow();
      } else if (map.getZoom() < ZOOM_REGION_THRESHOLD) {
        hidePowerLinesLow();
      }
    });
    return btn;
  },
  onRemove() {}
});
new L.Control.LowVoltageToggle({ position: "topright" }).addTo(map);

// Button for the key/legend of voltage lines
L.Control.VoltageKey = L.Control.extend({
  _panel: null,

  onAdd(map) {
    const btn = L.DomUtil.create("button", "leaflet-bar leaflet-control");
    btn.innerHTML = "&#9741;";
    btn.title = "Legende de la carte";
    btn.style.cssText = "width:30px;height:30px;cursor:pointer;font-size:13px;font-weight:700;line-height:28px;background:white;color:#333;border:none;text-align:center;";

    const panel = document.createElement("div");
    panel.hidden = true;
    panel.style.cssText = "position:absolute;right:42px;z-index:1000;background:rgba(12,22,14,0.96);border:1px solid rgba(34,197,94,0.18);border-radius:6px;padding:10px 14px 12px;white-space:nowrap;box-shadow:0 4px 20px rgba(0,0,0,0.55);";
    panel.innerHTML = `
      <strong style="display:block;font-size:0.7rem;font-weight:700;color:#e8f5eb;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">Lignes</strong>
      <div style="display:flex;flex-direction:column;gap:6px;">
        <div style="display:flex;align-items:center;gap:8px;font-size:0.75rem;color:#c8deca;">
          <span style="display:inline-block;width:22px;height:3px;border-radius:2px;background:#c73030;flex-shrink:0;"></span>&ge; 220 kV
        </div>
        <div style="display:flex;align-items:center;gap:8px;font-size:0.75rem;color:#c8deca;">
          <span style="display:inline-block;width:22px;height:3px;border-radius:2px;background:#b54eb2;flex-shrink:0;"></span>&ge; 310 kV
        </div>
        <div style="display:flex;align-items:center;gap:8px;font-size:0.75rem;color:#c8deca;">
          <span style="display:inline-block;width:22px;height:3px;border-radius:2px;background:#00c1cf;flex-shrink:0;"></span>&ge; 550 kV
        </div>
      </div>
      <div style="border-top:1px solid rgba(255,255,255,0.1);margin-bottom:10px;"></div>
      <strong style="display:block;font-size:0.7rem;font-weight:700;color:#e8f5eb;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;">Frontières</strong>
      <div style="display:flex;flex-direction:column;gap:6px;">
        <div style="display:flex;align-items:center;gap:8px;font-size:0.75rem;color:#c8deca;">
          <span style="display:inline-block;width:22px;height:3px;border-radius:2px;background:#e07000;flex-shrink:0;"></span>Pays avec bonne premiere ligne
        </div>
      </div>`;
    map.getContainer().appendChild(panel);
    this._panel = panel;

    L.DomEvent.disableClickPropagation(btn);
    L.DomEvent.on(btn, "click", () => {
      if (panel.hidden) {
        const btnRect = btn.getBoundingClientRect();
        const mapRect = map.getContainer().getBoundingClientRect();
        panel.style.top = (btnRect.top - mapRect.top) + "px";
      }
      panel.hidden = !panel.hidden;
    });
    return btn;
  },

  onRemove() {
    if (this._panel) { this._panel.remove(); this._panel = null; }
  }
});
new L.Control.VoltageKey({ position: "topright" }).addTo(map);

// Clickable layer for countries
const countriesLayer = L.geoJSON(null, {
  style: { color: "#38bdf8", weight: 0.7, fillOpacity: 0 }
}).addTo(map);

// Clickable layer for regions
const regionsLayer = L.geoJSON(null, {
  style: { color: "#1a4f80", weight: 0.6, fillOpacity: 0 }
});

// Switch between country and region layer based on zoom level.
// Also toggles 220 kV power lines: lazy-fetch on first crossing of the
// threshold, then hide/show on subsequent zooms (no refetch).
// If the user has explicitly turned on the 220 kV toggle, the layer stays
// visible at every zoom level.
map.on("zoomend", () => {
  const z = map.getZoom();
  if (z >= ZOOM_REGION_THRESHOLD) {
    loadRegionsOnce();
    if (!map.hasLayer(regionsLayer)) map.addLayer(regionsLayer);
    showPowerLinesLow();
  } else {
    if (map.hasLayer(regionsLayer)) map.removeLayer(regionsLayer);
    if (!STATE.lowVoltageForced) hidePowerLinesLow();
  }
});


// Functions for functionality of map

// Fetch countries geojson layer
function loadCountries() {
  return fetch("/data/countries.geojson")
    .then(r => r.json())
    .then(data => {
      countriesLayer.addData(data);
      countriesLayer.eachLayer(setupCountryLayer);
    })
    .catch(err => console.error("Countries GeoJSON failed:", err));
}

// Create countries layer based on geojson properties. Colour changes if layer has GFL
function setupCountryLayer(layer) {
  const iso  = layer.feature.properties.ISO_A2;
  const name = layer.feature.properties.NAME;
  if (iso) countryNameMap[iso.toUpperCase()] = name;

  layer.on("mouseover", () =>
    layer.setStyle({ fillColor: "#0ea5e9", fillOpacity: 0.28, weight: 1.5 }));
  layer.on("mouseout", () => {
    // Restore GFL orange fill rather than the default transparent fill.
    if (layer._isGFL) {
      layer.setStyle({ color: "#f97316", weight: 2, fillColor: "#fb923c", fillOpacity: 0.15 });
    } else {
      countriesLayer.resetStyle(layer);
    }
  });
  layer.on("click", () => handleAreaClick(iso, 2, layer));
}

// Fetches active Good First Line country names from Supabase.
async function fetchGFLCountries() {
  const SUPABASE_URL = "https://momhpgtitabhlpsxcqxh.supabase.co";
  const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vbWhwZ3RpdGFiaGxwc3hjcXhoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3MzUxODMsImV4cCI6MjA3NTMxMTE4M30.IUj10ikNkwip_iZsGxR8vUWNgRtK9aaiTovpTeKvm4c";
  try {
    const resp = await fetch(
      SUPABASE_URL + "/rest/v1/lines?select=country&status=neq.completed",
      { headers: { apikey: SUPABASE_KEY, Authorization: "Bearer " + SUPABASE_KEY } }
    );
    if (!resp.ok) return;
    const data = await resp.json();
    GFL_COUNTRY_NAMES = new Set(data.map(r => {
      const n = r.country.toLowerCase().trim();
      const normalized = GFL_NAME_NORMALISE[n] ?? n;
      return normalized.toLowerCase();}));
  } catch (err) {
    console.warn("GFL countries fetch failed (non-critical):", err);
  }
}

// Applies orange highlighting to any country layer whose name matches a GFL entry.
// Called after both loadCountries() and fetchGFLCountries() have resolved.
function applyGFLStyles() {
  countriesLayer.eachLayer(layer => {
    const name = layer.feature.properties.NAME;
    if (GFL_COUNTRY_NAMES.has(name.toLowerCase())) {
      layer._isGFL = true;
      layer.setStyle({ color: "#e07000", weight: 2, fillColor: "#ff8c00", fillOpacity: 0.15 });
    }
  });
}

// Fetches regionsv2.geojson on first zoom into region level.
async function loadRegionsOnce() {
  if (STATE.regionsLoaded) return;
  try {
    const resp = await fetch("/data/regionsv2.geojson");
    const data = await resp.json();
    regionsLayer.addData(data);
    regionsLayer.eachLayer(setupRegionLayer);
    STATE.regionsLoaded = true;
    if (map.getZoom() >= ZOOM_REGION_THRESHOLD && !map.hasLayer(regionsLayer)) {
      map.addLayer(regionsLayer);
    }
  } catch (err) {
    console.error("Regions GeoJSON failed:", err);
  }
}

// Power line overlay with two voltage tiers.
// High voltage here is 310 kV+: fetches afetr countries layer is loaded.
// Low voltage here is 220-309kV: lazy fetch on first zoom past ZOOM_REGION_THRESHOLD; hidden (but kept in memory) when zooming back out.
const powerLineStyle = f => {
  const v = parseInt(f.properties.v) || 0;
  if (v >= 550000) return { color: "#00c1cf", weight: 1.4, opacity: 0.75 };
  if (v >= 310000) return { color: "#b54eb2", weight: 1.1, opacity: 0.70 };
  return                   { color: "#c73030", weight: 0.8, opacity: 0.65 };
};

let powerHighLayer   = null;
let powerLowLayer    = null;
let powerLowFetching = false;

async function loadPowerLinesHigh() {
  if (powerHighLayer) return;
  try {
    const data = await fetch("/data/power_lines_high.geojson").then(r => r.json());
    powerHighLayer = L.geoJSON(data, {
      interactive: false,
      renderer: L.canvas({ padding: 0.5 }),
      style: powerLineStyle
    });
    powerHighLayer.addTo(map).bringToBack();
  } catch (err) {
    console.warn("Power lines (high) failed to load:", err);
  }
}

async function showPowerLinesLow() {
  if (powerLowLayer) {
    if (!map.hasLayer(powerLowLayer)) powerLowLayer.addTo(map).bringToBack();
    return;
  }
  if (powerLowFetching) return;
  powerLowFetching = true;
  try {
    const data = await fetch("/data/power_lines_low.geojson").then(r => r.json());
    powerLowLayer = L.geoJSON(data, {
      interactive: false,
      renderer: L.canvas({ padding: 0.5 }),
      style: powerLineStyle
    });
    powerLowLayer.addTo(map).bringToBack();
  } catch (err) {
    console.warn("Power lines (low) failed to load:", err);
  } finally {
    powerLowFetching = false;
  }
}

function hidePowerLinesLow() {
  if (powerLowLayer && map.hasLayer(powerLowLayer)) map.removeLayer(powerLowLayer);
}

// Create region clickable layer based on two properties from regionsv2 geojson
function setupRegionLayer(layer) {
  const iso  = layer.feature.properties.ISO_1;
  const name = layer.feature.properties.NAME_1;

  layer.on("mouseover", () => layer.setStyle({ fillColor: "#1a4f80", fillOpacity: 0.22, weight: 1.2 }));
  layer.on("mouseout",  () => regionsLayer.resetStyle(layer));
  layer.on("click",     () => handleAreaClick(iso, 4, layer));
}


// Left sidebar
async function initSidebar() {
  initEditorSwitch();
  await initQueryModes();
}

// Wires the JOSM / iD pill-style switch in the sidebar.
function initEditorSwitch() {
  document.querySelectorAll(".mi-switch-opt").forEach(btn => {
    btn.addEventListener("click", () => {
      STATE.editor = btn.dataset.editor;
      document.querySelectorAll(".mi-switch-opt")
              .forEach(b => b.classList.toggle("active", b === btn));

      const urlSection = document.getElementById("id-url-section");
      const warning    = document.getElementById("id-editor-warning");
      const opSect     = document.getElementById("section-overpass");

      if (STATE.editor === "id") {
        warning.classList.remove("hidden");
        opSect.style.opacity       = "0.45";
        opSect.style.pointerEvents = "none";
      } else {
        if (urlSection) urlSection.style.display = "none";
        warning.classList.add("hidden");
        opSect.style.opacity       = "";
        opSect.style.pointerEvents = "";
      }
    });
  });
}

// Fetches query folder names from GitHub and builds all sidebar buttons.
async function initQueryModes() {
  const TOOL_MODES = ["Osmose_issues","GEM_powerplants","MapYourSolar","Wikidata","GRW_wind","PPM"];
  let modes;
  try {
    const res   = await fetch(GITHUB_API_QUERIES);
    if (!res.ok) throw new Error("GitHub API error");
    const items = await res.json();
    modes = items
      .filter(i => i.type === "dir")
      .map(i => i.name)
      .filter(m => m !== "Osmose_issues");
    modes.sort((a, b) => {
      if (a === "Default") return -1;
      if (b === "Default") return  1;
      return a.localeCompare(b);
    });
  } catch (err) {
    console.error("Failed to load query modes:", err);
    return;
  }

  modes.splice(2, 0, ...TOOL_MODES);
  STATE.mode = modes.includes("Default") ? "Default" : modes[0];

  const overpassEl = document.getElementById("overpass-buttons");
  const toolEl     = document.getElementById("tool-buttons");

  for (const mode of modes) {
    const group = TOOL_MODES.includes(mode) ? buildToolButton(mode) : buildOverpassButton(mode);
    (TOOL_MODES.includes(mode) ? toolEl : overpassEl).appendChild(group);
  }

  const defaultBtn = overpassEl.querySelector("[data-mode='Default']");
  if (defaultBtn) defaultBtn.classList.add("active");
}

// Builds a sidebar button + version link for an Overpass QL query mode.
function buildOverpassButton(mode) {
  const label = mode === "Default" ? "Default Transmission (50 kV+)" : mode.replace(/_/g, " ");

  const btn = document.createElement("button");
  btn.className    = "mi-query-btn";
  btn.dataset.mode = mode;
  btn.textContent  = label;
  btn.addEventListener("click", () => selectMode(mode, btn));

  const verLink = document.createElement("a");
  verLink.className   = "mi-query-version";
  verLink.target      = "_blank";
  verLink.href        = "https://github.com/open-energy-transition/osm-grid-definition/tree/main/queries/" + encodeURIComponent(mode);
  verLink.textContent = "v…";
  fetchVersionCached(mode)
    .then(v  => { verLink.textContent = "v" + v; })
    .catch(() => { verLink.textContent = "v?"; });

  const group = document.createElement("div");
  group.className = "mi-query-group";
  group.append(btn, verLink);
  return group;
}

// Builds a sidebar button + source link for a hint/tool mode.
function buildToolButton(mode) {
  const LABELS = {
    Osmose_issues:   "Osmose Issues",
    GEM_powerplants: "Global Energy Monitor — Power Plants",
    MapYourSolar:    "Transition Zero — Solar Asset Mapper",
    Wikidata:        "Wikidata",
    GRW_wind:        "Global Renewables Watch — Wind Turbines",
    PPM:             "powerplantmatching"
  };
  const META = {
    Osmose_issues:   "<a href='https://osmose.openstreetmap.fr/' target='_blank'>osmose.openstreetmap.fr</a>",
    GEM_powerplants: "<a href='https://globalenergymonitor.org/' target='_blank'>globalenergymonitor.org</a> | CC BY 4.0",
    MapYourSolar:    "<a href='https://www.transitionzero.org/products/solar-asset-mapper/download' target='_blank'>transitionzero.org</a> | Q3-2025 | CC BY NC 4.0",
    Wikidata:        "<a href='https://github.com/open-energy-transition/osm-wikidata-toolset' target='_blank'>Repository</a>",
    GRW_wind:        "<a href='https://github.com/microsoft/global-renewables-watch/tree/main' target='_blank'>Global Renewables Watch</a> | Q2-2024",
    PPM:             "<a href='https://github.com/open-energy-transition/mapit-osm/tree/main' target='_blank'>Repository</a>"
  };

  const btn = document.createElement("button");
  btn.className    = "mi-query-btn";
  btn.dataset.mode = mode;
  btn.textContent  = LABELS[mode] || mode;
  btn.addEventListener("click", () => selectMode(mode, btn));

  const meta = document.createElement("div");
  meta.className = "mi-meta-link";
  meta.innerHTML = META[mode] || "";

  const group = document.createElement("div");
  group.className = "mi-query-group";
  group.append(btn, meta);

  // Sub-option panels for each hint goes inside their respective hint layer group
  const PANEL_IDS = {
    Osmose_issues:   "osmose-panel",
    GEM_powerplants: "gem-panel",
    MapYourSolar:    "solar-panel",
    Wikidata:        "wikidata-panel",
    GRW_wind:        "wind-panel",
    PPM:             "ppm-panel",
  };
  const panelEl = document.getElementById(PANEL_IDS[mode]);
  if (panelEl) group.appendChild(panelEl);

  return group;
}

// Updates active button state and shows/hides the relevant sub-option panel.
function selectMode(mode, activeBtn) {
  STATE.mode = mode;
  document.querySelectorAll("#overpass-buttons .mi-query-btn, #tool-buttons .mi-query-btn")
           .forEach(b => b.classList.toggle("active", b === activeBtn));

  const PANEL_MAP = {
    Osmose_issues:   "osmose-panel",
    Wikidata:        "wikidata-panel",
    PPM:             "ppm-panel",
    GEM_powerplants: "gem-panel",
    MapYourSolar:    "solar-panel",
    GRW_wind:        "wind-panel"
  };
  Object.entries(PANEL_MAP).forEach(([m, id]) => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle("hidden", m !== mode);
  });

  // Auto-expand the hints section when a tool is selected.
  if (mode in PANEL_MAP) {
    document.getElementById("section-hints").classList.remove("collapsed");
  }
}

// Fetches and caches the version string for an overpass mode folder, from the github repo.
async function fetchVersionCached(mode) {
  if (STATE.versionCache[mode]) return STATE.versionCache[mode];
  const r = await fetch(RAW_BASE + "/" + mode + "/version.txt");
  if (!r.ok) throw new Error("version not found");
  const v = (await r.text()).trim();
  STATE.versionCache[mode] = v;
  return v;
}

// Called by onclick on collapsible section header buttons.
// Toggles the collapsed class on the parent .mi-section.
function toggleSection(headerBtn) {
  headerBtn.closest(".mi-section").classList.toggle("collapsed");
}

// Shows/hides the sidebar on mobile (small screens only).
function toggleMobileSidebar() {
  document.getElementById("mapit-sidebar").classList.toggle("open");
}


// Introudciton info card

function renderInfoSlide() {
  const slide = INFO_SLIDES[STATE.infoSlide];
  document.getElementById("info-title").textContent   = slide.title;
  document.getElementById("info-card-body").innerHTML = slide.content;
  document.getElementById("info-pager").textContent   =
    (STATE.infoSlide + 1) + " / " + INFO_SLIDES.length;
  document.getElementById("info-prev").disabled = STATE.infoSlide === 0;
  document.getElementById("info-next").disabled = STATE.infoSlide === INFO_SLIDES.length - 1;
}

function infoCardPrev() {
  if (STATE.infoSlide > 0) { STATE.infoSlide--; renderInfoSlide(); }
}

function infoCardNext() {
  if (STATE.infoSlide < INFO_SLIDES.length - 1) { STATE.infoSlide++; renderInfoSlide(); }
}

// Collapses or expands the info card body text.
function toggleInfoCard() {
  STATE.infoCollapsed = !STATE.infoCollapsed;
  document.getElementById("info-card-body").classList.toggle("hidden", STATE.infoCollapsed);
  document.getElementById("info-toggle").classList.toggle("rotated", STATE.infoCollapsed);
}


// Country panel (slides up when a country is clicked)
function showCountryPanel(name, iso2, bodyHtml) {
  document.getElementById("country-name").textContent = name;
  document.getElementById("country-flag").src =
    "https://flagcdn.com/28x21/" + (iso2 || "un").toLowerCase() + ".png";
  updateCountryPanel(bodyHtml);
  document.getElementById("country-panel").classList.add("open");
}

function updateCountryPanel(bodyHtml) {
  document.getElementById("country-panel-body").innerHTML = bodyHtml;
}

function hideCountryPanel() {
  document.getElementById("country-panel").classList.remove("open");
}

// Overlay boxes for legend / hotkeys / guidelines / practices / calendar)
function buildHotkeysTable() {
  const rows = [
    ["S","Sélectionner des objets"], ["A","Améliorer : 'Mode Standard', il va tracer des lignes 'connectées'"],
    ["Ctrl+C","Copier"], ["Ctrl+V","Coller"],
    ["Ctrl+F","Rechercher (Mode Expert)"], ["Ctrl+Z","Annuler"], ["Ctrl+Y","Refaire"],
    ["Ctrl+Shift+C","Copier coordonnées"], ["Ctrl+W","	Basculer le mode d'affichage "],
    ["Ctrl+H","Historique"], ["Ctrl+U","Mettre à jour les données"],
    ["Shift+V","Valider les données"], ["Tab","Afficher la barre d'outils"]
  ].map(([k, d]) => `<tr><td><code>${k}</code></td><td>${d}</td></tr>`).join("");
  return `<table class="mi-hotkeys-table"><thead><tr><th>Key</th><th>Action</th></tr></thead><tbody>${rows}</tbody></table>`;
}

// Static registry for each overlay. slides: array = multi-page; null = single page.
const OVERLAY_REGISTRY = {
  legend: {
    title: "Map Legend",
    html:  "<img src='https://raw.githubusercontent.com/open-energy-transition/color-my-grid/refs/heads/main/legend/power-grid-legend.svg' alt='Power Grid Legend' style='max-width:100%;display:block;margin:auto;'>",
    slides: null
  },
  hotkeys: {
    title:  "JOSM Hotkeys",
    html:   buildHotkeysTable(),
    slides: null
  },
  guidelines: {
    title: "Mapping Guidelines",
    html: `<ul class="mi-guideline-list">
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_networks" target="_blank">Power networks</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines" target="_blank">Power networks / Guidelines</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Power_lines" target="_blank">Guidelines / Power lines</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Substations" target="_blank">Guidelines / Substations</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_generation/Guidelines/Hydropower" target="_blank">Guidelines / Hydropower</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_generation/Guidelines/Solar_plants" target="_blank">Guidelines / Solar plants</a></li>
      <li><a href="https://wiki.openstreetmap.org/wiki/Power_networks/Guidelines/Interconnector" target="_blank">Guidelines / Interconnectors</a></li>
      <li><a href="https://community.openstreetmap.org/t/clarifying-power-pole-vs-power-tower/127382" target="_blank">Clarifying power=pole vs power=tower</a></li>
    </ul>`,
    slides: null
  },
  practices: {
    title:  PRACTICES_SLIDES[0].title,
    html:   PRACTICES_SLIDES[0].content,
    slides: PRACTICES_SLIDES
  },
  calendar: {
    title: "Community Calendar",
    html:  "<iframe src='https://calendar.google.com/calendar/embed?src=mapyourgrid%40gmail.com&ctz=Europe%2FBerlin' height='480'></iframe>",
    slides: null
  }
};

// Opens the modal overlay for the given registry key.
function openOverlay(key) {
  const cfg = OVERLAY_REGISTRY[key];
  if (!cfg) return;

  document.getElementById("overlay-title").textContent = cfg.title;
  document.getElementById("overlay-body").innerHTML    = cfg.html;

  const nav = document.getElementById("overlay-slide-nav");
  if (cfg.slides) {
    STATE.overlaySlides   = cfg.slides;
    STATE.overlaySlideIdx = 0;
    nav.classList.remove("hidden");
    renderOverlaySlide();
  } else {
    STATE.overlaySlides = null;
    nav.classList.add("hidden");
  }

  document.getElementById("mapit-overlay").classList.remove("hidden");
}

function renderOverlaySlide() {
  const slide = STATE.overlaySlides[STATE.overlaySlideIdx];
  document.getElementById("overlay-title").textContent = slide.title;
  document.getElementById("overlay-body").innerHTML    = slide.content;
  document.getElementById("overlay-pager").textContent =
    (STATE.overlaySlideIdx + 1) + " / " + STATE.overlaySlides.length;
}

function overlayPrev() {
  if (STATE.overlaySlideIdx > 0) { STATE.overlaySlideIdx--; renderOverlaySlide(); }
}

function overlayNext() {
  if (STATE.overlaySlides && STATE.overlaySlideIdx < STATE.overlaySlides.length - 1) {
    STATE.overlaySlideIdx++;
    renderOverlaySlide();
  }
}

// Closes the overlay. When triggered by a backdrop click, only closes if the
// backdrop itself (not the content box inside) was the target.
function closeOverlay(event) {
  if (event && event.target !== document.getElementById("mapit-overlay")) return;
  document.getElementById("mapit-overlay").classList.add("hidden");
}


// Interactive click handler
function getOverride(name, kind) {
  if (!name || !kind) return null;
  return (OVERRIDES[kind] && OVERRIDES[kind][name]) || null;
}

// Unified handler for both country (level 2) and region (level 4) clicks.
async function handleAreaClick(iso, level, layer) {
  const name    = level === 2 ? layer.feature.properties.NAME : layer.feature.properties.NAME_1;
  const sovName = layer.feature.properties.SOVEREIGNT;
  const iso2    = level === 2 ? iso : (iso ? iso.split(/[-_]/)[0].toUpperCase() : null);

  layer.setStyle({ color: "#ff7800", weight: 2 });
  showCountryPanel(name, iso2, "<p class='loading'>Loading… (disable ad blocker if nothing happens)</p>");
  if (typeof umami !== "undefined") umami.track("map-click");

  let showSuccess = true;
  try {
    if      (STATE.mode === "Osmose_issues")   await handleOsmoseClick(iso, level, layer, name, sovName);
    else if (STATE.mode === "GEM_powerplants") await fetchGEMAndDownload(sovName);
    else if (STATE.mode === "MapYourSolar")    await fetchSolarAndDownload(getOverride(sovName, "MapYourSolar") || sovName);
    else if (STATE.mode === "Wikidata")        await fetchWikidataAndDownload(getOverride(sovName, "wikidata") || sovName);
    else if (STATE.mode === "GRW_wind")        await fetchWindAndDownload(sovName);
    else if (STATE.mode === "PPM")             await fetchPPMAndDownload(sovName);
    else {
      if (!iso) {
        updateCountryPanel("<p>No ISO code for this region — click the country boundary for national data.</p>");
        showSuccess = false;
      } else {
        let tpl = await fetchQuery(STATE.mode, level);
        tpl = tpl.replace(/\$\{iso\}/g, iso);
        sendToJosm(tpl, name);
      }
    }
  } catch (err) {
    updateCountryPanel("<p>&#9888; Error: some hint layers only work at national level.</p>");
    showSuccess = false;
  }

  setTimeout(() => {
    layer.setStyle({ color: "#2c6fa0", weight: 0.8 });
    if (showSuccess) updateCountryPanel(buildSuccessHtml());
  }, 2000);
}

// Country panel 
function buildSuccessHtml() {
  if (STATE.editor === "id") {
    return "<div class='popup-success'><p>&#127881; <strong>Great!</strong> Copy the URL in the sidebar. In iD Editor, click \"Map Data\" → three dots → \"Custom map data\" and paste.</p></div>";
  }
  return `<div class="popup-success">
    <p>Ouvre <a href="https://josm.openstreetmap.de/" target="_blank">JOSM</a> — certains pays prennent plus de 60 secondes à charger.</p>
    <ol>
      <li>Le serveur Overpass peut être occupé — essaie encore une/deux fois.</li>
      <li>Assure toi que le Controle à Distance est activé dans JOSM Preferences.</li>
      <li>Certaines couches d'outils ne marchent qu'au niveau national.</li>
      <li>Regarder <a href="/starter-kit/">Tutos</a> pour plus d'aide.</li>
    </ol>
  </div>`;
}

// Resolves the country name for Osmose region queries via multiple fallbacks.
async function handleOsmoseClick(iso, level, layer, regionName, sovName) {
  if (level === 4) {
    let country = layer.feature.properties.COUNTRY || null;
    if (!country && typeof iso === "string" && /[-_]/.test(iso)) {
      const parentIso = iso.split(/[-_]/)[0].toUpperCase();
      country = countryNameMap[parentIso] || null;
    }
    if (!country) country = layer.feature.properties.SOVEREIGNT || sovName;
    await fetchOsmoseAndDownload(country, regionName);
  } else {
    await fetchOsmoseAndDownload(sovName, null);
  }
}


// JOSM remote control functions

// Sends a URL to JOSM via a hidden iframe. The iframe self-destructs after 1 s.
function josmRequest(url) {
  const iframe = document.createElement("iframe");
  iframe.style.display = "none";
  iframe.src = url;
  document.body.appendChild(iframe);
  setTimeout(() => iframe.remove(), 1000);
}

// Loads geojsons to josm, and adds hashtags in the chnageset
function sendUrlToJosm(dataUrl, layerName, geojson) {
  josmRequest(
    "http://localhost:8111/import?new_layer=true" +
    "&layer_name=" + encodeURIComponent(layerName) +
    "&changeset_tags=hashtags=mapyourgrid" +
    "&url=" + encodeURIComponent(dataUrl) +
    (geojson ? "&format=geojson" : "")
  );
}

// Loads overpass queries to JOSM, imagery layers, and hashtag
function sendToJosm(query, areaName) {
  josmRequest(
    "http://localhost:8111/import?new_layer=true" +
    "&layer_name=" + encodeURIComponent(areaName) +
    "&changeset_tags=hashtags=mapyourgrid" +
    "&url=" + encodeURIComponent("https://overpass-api.de/api/interpreter?data=" + encodeURIComponent(query))
  );
  josmRequest("http://localhost:8111/imagery?id=Mapbox");
  josmRequest("http://localhost:8111/imagery?id=Bing");
  josmRequest("http://localhost:8111/imagery?id=EsriWorldImagery");
}

// Shows the data URL inside the sidebar iD URL box (between Overpass and Hints sections).
function displayUrlForId(url) {
  const section = document.getElementById("id-url-section");
  const input   = document.getElementById("url-display");
  const copyBtn = document.getElementById("copy-btn");
  if (section) section.style.display = "";  // reveal the section wrapper
  input.value = url;
  copyBtn.textContent = "Copy";
  copyBtn.onclick = () =>
    navigator.clipboard.writeText(url)
      .then(() => { copyBtn.textContent = "Copied!"; })
      .catch(() => { alert("Copy failed — select the text and press Ctrl+C."); });
}


// Fetching the data for each mode and hint

// Fetches overpass query (based on admin level)
async function fetchQuery(mode, adminLevel) {
  const r = await fetch(RAW_BASE + "/" + mode + "/admin" + adminLevel + ".overpassql");
  if (!r.ok) throw new Error("Query not found: " + mode + "/admin" + adminLevel);
  return r.text();
}

// Osmose:
    //  Converts a display name to the slug Osmose uses for country/region filters.
    // e.g. "MatoGrossodoSul" → "mato_grosso_do_sul"
function slugifyForOsmose(name) {
  if (!name) return "";
  let s = String(name);
  s = s.replace(/([a-z0-9])([A-Z])/g, "$1_$2");
  s = s.replace(/([A-Z])([A-Z][a-z])/g, "$1_$2");
  s = s.normalize("NFD").replace(/[̀-ͯ]/g, "");
  s = s.replace(/[^0-9A-Za-z]+/g, "_");
  return s.replace(/_+/g, "_").replace(/^_|_$/, "").toLowerCase();
}

// USes osmose API to fetch the issues based on certain classes (power), and location
async function fetchOsmoseAndDownload(countryName, regionName) {
  const sel = document.getElementById("osmoseIssue");
  if (!sel || !sel.value) { alert("Please select an issue type."); return; }
  const [item, cls] = sel.value.split(":");
  const countryToken = getOverride(countryName, "osmoseCountries") || slugifyForOsmose(countryName);
  let base = countryToken;
  if (regionName) {
    base = countryToken + "_" + (getOverride(regionName, "osmoseRegions") || slugifyForOsmose(regionName));
  }
  if (!base.endsWith("*")) base += "*";
  const apiUrl =
    "https://osmose.openstreetmap.fr/api/0.3/issues.geojson?" +
    "country=" + encodeURIComponent(base) +
    "&item=" + item + "&class=" + cls + "&limit=5000&useDevItem=all";
  if (STATE.editor === "id") { displayUrlForId(apiUrl); return; }
  const resp = await fetch(apiUrl);
  if (!resp.ok) throw new Error("Osmose API error");
  const geojson = await resp.json();
  if (!geojson.features || !geojson.features.length) {
    alert("No Osmose issues found for \"" + sel.options[sel.selectedIndex].text + "\" in " + countryName + ".");
    return;
  }
  const layerName = (regionName ? countryName + "_" + regionName : countryName).replace(/\s+/g, "_") +
                    "-osmose-" + item + "-" + cls;
  sendUrlToJosm(apiUrl, layerName, true);
}

// Fetches the GEM power plant database layer from osm-grid-definition repo
async function fetchGEMAndDownload(sovName) {
  const url = "https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/main/GEM/GEM-Global-Integrated-Power-February-2025-update-II/" +
              sovName.replace(/\s+/g, "_") + ".geojson";
  const resp = await fetch(url, { method: "HEAD" });
  if (!resp.ok) { alert("No GEM file for " + sovName + "."); return; }
  if (STATE.editor === "id") { displayUrlForId(url); return; }
  sendUrlToJosm(url, sovName + "-GEM");
}

// Fetches the Transition Zero Solar plant database layer from osm-grid-definition repo
async function fetchSolarAndDownload(sovName) {
  const url = "https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/main/TZ-Solar/TZ-Q32025/" +
              sovName.replace(/\s+/g, "_") + ".geojson";
  const resp = await fetch(url, { method: "HEAD" });
  if (!resp.ok) { alert("No Solar file for " + sovName + "."); return; }
  if (STATE.editor === "id") { displayUrlForId(url); return; }
  sendUrlToJosm(url, sovName + "-solarTZ");
}

// Fetches the wikidata geojsons database layer from osm-grid-definition repo
async function fetchWikidataAndDownload(sovName) {
  const type = document.getElementById("wikidataType").value;
  const FOLDERS = {
    "All power-related infrastructure": "/output_by_qid_v2/geojson_by_country",
    "substations":  "/substations/geojson_by_country",
    "powerplants":  "/output_by_qid/Q159719_power_plant"
  };
  const folder = FOLDERS[type];
  if (!folder) { alert("Unknown Wikidata type."); return; }
  const url = "https://raw.githubusercontent.com/open-energy-transition/osm-wikidata-toolset/main/" +
              folder + "/" + sovName.replace(/\s+/g, "_") + ".geojson";
  const resp = await fetch(url, { method: "HEAD" });
  if (!resp.ok) { alert("No Wikidata file for " + sovName + "."); return; }
  if (STATE.editor === "id") { displayUrlForId(url); return; }
  sendUrlToJosm(url, sovName + "-wikidata");
}

// Fetches the Wind renewables watch database layer from osm-grid-definition repo
async function fetchWindAndDownload(sovName) {
  const url = "https://raw.githubusercontent.com/open-energy-transition/osm-grid-definition/main/wind-renewables-watch/2024-q2v1/" +
              sovName.replace(/\s+/g, "_") + ".geojson";
  const resp = await fetch(url, { method: "HEAD" });
  if (!resp.ok) { alert("No Wind file for " + sovName + "."); return; }
  if (STATE.editor === "id") { displayUrlForId(url); return; }
  sendUrlToJosm(url, sovName + "-windGRW");
}

// Fetches the PPM geojson database layer from osm-grid-definition repo
async function fetchPPMAndDownload(sovName) {
  const url = "https://raw.githubusercontent.com/open-energy-transition/mapit-osm/main/ppm_rejected_geojson_by_country/" +
              sovName.replace(/\s+/g, "_") + ".geojson";
  const resp = await fetch(url);
  if (!resp.ok) { alert("No PPM file for " + sovName + "."); return; }
  if (STATE.editor === "id") { displayUrlForId(url); return; }
  sendUrlToJosm(url, sovName + "-ppm");
}


// Bootstrap

document.addEventListener("DOMContentLoaded", async () => {
  // Measure actual MkDocs header + announcement banner height and apply to root.
  const header = document.querySelector(".md-header");
  const banner = document.querySelector(".md-banner");
  let topOffset = 0;
  if (header) topOffset += header.getBoundingClientRect().height;
  if (banner) topOffset += banner.getBoundingClientRect().height;
  document.getElementById("mapit-root").style.top = topOffset + "px";

  renderInfoSlide();

  // Countries + GFL highlighting must be ready before power lines start —
  // otherwise the heavy fetch competes with the click-target layer the user
  // needs first. Power lines fire-and-forget so they don't block the sidebar.
  await Promise.all([fetchGFLCountries(), loadCountries()]);
  applyGFLStyles();
  loadPowerLinesHigh();

  initSidebar().catch(console.error);
});
</script>
