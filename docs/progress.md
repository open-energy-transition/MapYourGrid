<div class="page-headers">
<h1>Our Progress</h1>
</div>

MapYourGrid measures its progress at user, hashtag and country level. If you use our tools and training courses, we would be honored if you support our KPI. Just use the #MapYourGrid hashtag in your changesets or add your user id to our [KPI script](https://github.com/open-energy-transition/MapYourGrid/blob/main/.github/workflows/update-tower-count.yml). If you would like to contribute to our development or keep up to date with our progress, take a look at our public [organization project management in GitHub](https://github.com/orgs/open-energy-transition/projects).

<!-- Progress Bars Section -->
## **<div class="tools-header">Community Mapping Progress </div>**

<div class="progress-section"> 
   <button id="refresh-btn" style="margin-bottom:1rem;">
     🔄 Refresh stats (only click if the bars are not "loading...")
   </button>


  <div class="progress-item">
    <label>Contributors mapping with <code>#mapyourgrid</code> and <code>#ohmygrid</code> hashtag:</label>
    <div class="progress"> <div class="progress-bar" id="contributors-bar" style="background-color: #28a745;"></div> </div>
    <span id="contributors-count">Loading…</span>
  </div>

  <div class="progress-item">
    <label>Total Edits for <code>#mapyourgrid</code> hashtag:</label>
    <div class="progress">
      <div class="progress-bar" id="edits-bar" style="background-color: #28a745;"></div> </div>
    <span id="edits-count">Loading…</span>
  </div>

  <div class="progress-item">
    <label>Total estimated power towers added by mappers of the MapYourGrid funding organisations:</label>
    <div class="progress">
      <div class="progress-bar" id="tower-bar" style="background-color: #17a2b8;"></div>
    </div>
    <span id="tower-count">Loading…</span>
    <br>
    <span id="tower-updated" style="font-size:0.8em; color:#666">Last updated: —</span>
  </div>

  <div class="progress-item">
    <label>Total estimated length of power lines added by mappers of the MapYourGrid funding organisations:</label>
    <div class="progress">
      <div class="progress-bar" id="line-length-bar" style="background-color: #17a2b8;"></div>
    </div>
    <span id="line-length-count">Loading…</span><br>
    <span id="line-length-updated" style="font-size:0.8em; color:#666">
      Last updated: —
    </span>
  </div>

  <div class="progress-item">
    <label>Total Estimated Global Power Capacity added by mappers of the MapYourGrid funding organisations:</label>
    <div class="progress">
      <div class="progress-bar" id="plant-capacity-bar" style="background-color: #17a2b8;"></div>
    </div>
    <span id="plant-capacity-count">Loading…</span>
    <br>
    <span id="plant-capacity-updated" style="font-size:0.8em; color:#666">Last updated: —</span>
  </div>

  <div class="progress-item">
    <label>Total estimated power towers added by people using the <code>#MapYourGrid</code>:</label>
    <div class="progress">
      <div class="progress-bar" id="community-tower-bar" style="background-color: #28a745;"></div>
    </div>
    <span id="community-tower-count">Loading…</span>
    <br>
    <span id="community-tower-updated" style="font-size:0.8em; color:#666">Last updated: —</span>
  </div>

  <div class="progress-item">
    <label>Total estimated length of power lines added by people using the <code>#MapYourGrid</code>:</label>
    <div class="progress">
      <div class="progress-bar" id="community-line-length-bar" style="background-color: #28a745;"></div>
    </div>
    <span id="community-line-length-count">Loading…</span><br>
    <span id="community-line-length-updated" style="font-size:0.8em; color:#666">
      Last updated: —
    </span>
  </div>


</div>


<script>

    // —— CONFIGURE THESE GOALS ——
  const CONTRIBUTORS_GOAL = 1;
  const EDITS_GOAL        = 10000;
  const TOWER_GOAL        = 10000;
  const LINE_LENGTH_GOAL = 5000;
  const COMMUNITY_TOWER_GOAL = 5000;
  const COMMUNITY_LINE_LENGTH_GOAL = 2500;
  const PLANT_CAPACITY_GOAL = 5000

   // —— UPDATE Ohsome (#MapYourGrid) ——
  async function updateOhsome() {
    const contribCountEl = document.getElementById('contributors-count');
    const editsCountEl   = document.getElementById('edits-count');
    const contribBar     = document.getElementById('contributors-bar');
    const editsBar       = document.getElementById('edits-bar');

    // set loading
    contribCountEl.textContent = 'Loading…';
    editsCountEl.textContent   = 'Loading…';
    contribBar.style.width     = '0%';
    editsBar.style.width       = '0%';

    try {
      const startDate = '2025-03-12T22:00:00Z';
      const endDate   = new Date().toISOString();
      const hashtags = ['mapyourgrid', 'ohmygrid'];
      const url       = `https://stats.now.ohsome.org/api/stats/MapYourGrid?startdate=${startDate}&enddate=${endDate}`;
      const urls = hashtags.map(tag => `https://stats.now.ohsome.org/api/stats/${tag}?startdate=${startDate}&enddate=${endDate}`);

      const responses = await Promise.all(urls.map(url => fetch(url)));
      for (const resp of responses) {
        if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
      }

      const dataArray = await Promise.all(responses.map(resp => resp.json()));

      // Aggregate the results (sum of users and edits)
      const total = dataArray.reduce((acc, data) => {
        acc.users += data.result.users ?? 0;
        acc.edits += data.result.edits ?? 0;
        return acc;
      }, { users: 0, edits: 0 });

      const { users, edits } = total;

      // write DOM
      contribCountEl.textContent = users.toLocaleString();
      editsCountEl.textContent   = edits.toLocaleString('en-US');

      contribBar.style.width = Math.min(100, users / CONTRIBUTORS_GOAL * 100) + '%';
      editsBar.style.width   = Math.min(100, edits / EDITS_GOAL        * 100) + '%';

      // cache
      localStorage.setItem('Combined-ohsome', JSON.stringify({
        users,
        edits,
        ts: Date.now()
      }));
    } catch (err) {
      console.error('Ohsome error', err);
      contribCountEl.textContent = 'Error';
      editsCountEl.textContent = 'Error';
    }
  }

 async function loadTowerCount() {
  const towerCountEl   = document.getElementById('tower-count');
  const towerBar       = document.getElementById('tower-bar');
  const towerUpdatedEl = document.getElementById('tower-updated');

  towerCountEl.textContent   = 'Loading…';
  towerBar.style.width       = '0%';
  towerUpdatedEl.textContent = 'Last updated: —';

  try {
    const resp = await fetch('/data/tower-count.json');
    if (!resp.ok) throw new Error(resp.statusText);
    const { towerCount: count, updated } = await resp.json();

    towerCountEl.textContent   = count.toLocaleString('en-US');
    towerBar.style.width       = Math.min(100, count / TOWER_GOAL * 100) + '%';
    towerUpdatedEl.textContent = `Last updated: ${new Date(updated).toLocaleString()}`;
  }
  catch(err) {
    console.error('Error loading tower count', err);
    towerCountEl.textContent = 'Error';
    towerUpdatedEl.textContent = '';
  }
}

async function loadLineLength() {
  const lengthEl      = document.getElementById('line-length-count');
  const lengthBar     = document.getElementById('line-length-bar');
  const updatedEl     = document.getElementById('line-length-updated');

  lengthEl.textContent   = 'Loading…';
  lengthBar.style.width  = '0%';
  updatedEl.textContent  = 'Last updated: —';

  try {
    const resp = await fetch('/data/line-length.json');
    if (!resp.ok) throw new Error(resp.statusText);
    const data = await resp.json();
    const { lengthKm, mediumHighVoltageKm, percentageOfMediumHigh, updated } = data;

    // Always show the length, even if percentage calculation failed
    let displayText = `${Math.round(lengthKm).toLocaleString('en-US')} km`;

   // Only add percentage if we have valid data
    if (percentageOfMediumHigh !== null && percentageOfMediumHigh !== undefined && mediumHighVoltageKm) {
      displayText += `<br><small style="color: #666; font-size: 0.85em;">${percentageOfMediumHigh}% of all high-voltage lines in OpenStreetMap (source: openinframap.org)</small>`;
    }

    lengthEl.innerHTML = displayText;
    lengthBar.style.width  = Math.min(100, lengthKm / LINE_LENGTH_GOAL * 100) + '%';
    updatedEl.textContent  = `Last updated: ${new Date(updated).toLocaleString()}`;
  } catch(err) {
    console.error('Error loading line length', err);
    lengthEl.textContent = 'Error';
    updatedEl.textContent = '';
  }
}

async function loadCommunityStats() {
  const towerCountEl = document.getElementById('community-tower-count');
  const towerBar = document.getElementById('community-tower-bar');
  const communityTowerUpdatedEl = document.getElementById('community-tower-updated'); // Correct ID for tower updated

  const lengthEl = document.getElementById('community-line-length-count');
  const lengthBar = document.getElementById('community-line-length-bar');
  const communityLineLengthUpdatedEl = document.getElementById('community-line-length-updated'); // Correct ID for line length updated

  // Set initial loading states
  towerCountEl.textContent = 'Loading…';
  towerBar.style.width = '0%';
  communityTowerUpdatedEl.textContent = 'Last updated: —';

  lengthEl.textContent = 'Loading…';
  lengthBar.style.width = '0%';
  communityLineLengthUpdatedEl.textContent = 'Last updated: —';

  try {
    const resp = await fetch('/data/community-stats.json');
    if (!resp.ok) throw new Error(resp.statusText);
    const data = await resp.json();

    // Correctly extract data based on your provided JSON structure
    const towerCount = data.towerCount ?? 0;
    const lengthKm = data.lengthKm ?? 0;
    const updated = data.updated;

    // Update Community Towers
    towerCountEl.textContent = towerCount.toLocaleString('en-US');
    towerBar.style.width = Math.min(100, towerCount / COMMUNITY_TOWER_GOAL * 100) + '%';
    communityTowerUpdatedEl.textContent = `Last updated: ${new Date(updated).toLocaleString()}`;

    // Update Community Line Length
    lengthEl.textContent = `${lengthKm.toLocaleString('en-US')} km`;
    lengthBar.style.width = Math.min(100, lengthKm / COMMUNITY_LINE_LENGTH_GOAL * 100) + '%';
    communityLineLengthUpdatedEl.textContent = `Last updated: ${new Date(updated).toLocaleString()}`;

    // Cache community stats
    localStorage.setItem('MapYourGrid-community-stats', JSON.stringify({
      communityTowerCount: towerCount,
      communityLineLengthKm: lengthKm,
      updated: updated, // Store the actual updated timestamp from JSON
      ts: Date.now() // Store current time for cache age
    }));

  } catch (err) {
    console.error('Error loading community stats', err);
    // Change to 'Error' for clarity when something goes wrong fetching data
    towerCountEl.textContent = 'Error';
    lengthEl.textContent = 'Error';
    communityTowerUpdatedEl.textContent = ''; // Clear timestamp on error
    communityLineLengthUpdatedEl.textContent = ''; // Clear timestamp on error
  }
}

async function loadPlantCapacity() {
    const capacityCountEl = document.getElementById('plant-capacity-count');
    const capacityBar = document.getElementById('plant-capacity-bar');
    const capacityUpdatedEl = document.getElementById('plant-capacity-updated');

    capacityCountEl.textContent = 'Loading…';
    capacityBar.style.width = '0%';
    capacityUpdatedEl.textContent = 'Last updated: —';

    try {
      const resp = await fetch('/data/plant-capacity.json');
      if (!resp.ok) throw new Error(resp.statusText);
      const { total_capacity_mw, updated } = await resp.json();

      capacityCountEl.textContent = `${total_capacity_mw.toLocaleString('en-US')} MW`;
      capacityBar.style.width = Math.min(100, total_capacity_mw / PLANT_CAPACITY_GOAL * 100) + '%';
      capacityUpdatedEl.textContent = `Last updated: ${new Date(updated).toLocaleString()}`;
    } catch (err) {
      console.error('Error loading plant capacity', err);
      capacityCountEl.textContent = 'Error';
      capacityUpdatedEl.textContent = '';
    }
  }

// —— MAIN & CACHE HANDLING ——
  function attemptCacheLoad(id, maxAgeMs) {
    try {
      const raw = localStorage.getItem(id);
      if (!raw) return null;
      const { ts, ...rest } = JSON.parse(raw);
      if (Date.now() - ts > maxAgeMs) return null;
      return rest;
    }
    catch { return null; }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // 1h cache
    const oneHour = 60*60*1000;

    // try Ohsome cache
    const oCache = attemptCacheLoad('MapYourGrid-ohsome', oneHour);
    if (oCache) {
      // populate from cache
      document.getElementById('contributors-count').textContent = oCache.users.toLocaleString('en-US');
      document.getElementById('edits-count').textContent       = oCache.edits.toLocaleString('en-US');
      document.getElementById('contributors-bar').style.width = Math.min(100, oCache.users / CONTRIBUTORS_GOAL * 100) + '%';
      document.getElementById('edits-bar').style.width       = Math.min(100, oCache.edits / EDITS_GOAL * 100) + '%';
    } else {
      updateOhsome();
    }

    // try Towers cache
    const tCache = attemptCacheLoad('MapYourGrid-towers', oneHour);
    if (tCache) {
      document.getElementById('tower-count').textContent = tCache.count.toLocaleString('en-US');
      document.getElementById('tower-bar').style.width   = Math.min(100, tCache.count / TOWER_GOAL * 100) + '%';
      document.getElementById('tower-updated').textContent = `Last updated: ${new Date(tCache.updated).toLocaleString()}`; // Populate updated from cache
    } else {
      loadTowerCount();
    }

    loadLineLength();
    loadPlantCapacity();

    // Try Community Stats cache
    const csCache = attemptCacheLoad('MapYourGrid-community-stats', oneHour);
    if (csCache) {
      document.getElementById('community-tower-count').textContent = csCache.communityTowerCount.toLocaleString('en-US');
      document.getElementById('community-tower-bar').style.width = Math.min(100, csCache.communityTowerCount / COMMUNITY_TOWER_GOAL * 100) + '%';
      document.getElementById('community-tower-updated').textContent = `Last updated: ${new Date(csCache.updated).toLocaleString()}`;

      document.getElementById('community-line-length-count').textContent = `${csCache.communityLineLengthKm.toLocaleString('en-US')} km`;
      document.getElementById('community-line-length-bar').style.width = Math.min(100, csCache.communityLineLengthKm / COMMUNITY_LINE_LENGTH_GOAL * 100) + '%';
      document.getElementById('community-line-length-updated').textContent = `Last updated: ${new Date(csCache.updated).toLocaleString()}`;
    } else {
      loadCommunityStats();
    }


    // refresh button now refreshes both
    const btn = document.getElementById('refresh-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        localStorage.removeItem('MapYourGrid-ohsome');
        localStorage.removeItem('MapYourGrid-towers');
        localStorage.removeItem('MapYourGrid-line-length');
        localStorage.removeItem('MapYourGrid-community-stats'); // Clear community stats cache
        updateOhsome();
        loadTowerCount();
        loadLineLength();
        loadCommunityStats(); 
        loadPlantCapacity();
      });
    }
  });
</script>

You can find more stats for #mapyourgrid at [OhsomeNowstats](https://stats.now.ohsome.org/dashboard#hashtag=MapYourGrid&start=2025-03-12T22:00:00Z&end=2025-05-14T21:59:59Z&interval=P1M&countries=&topics=).

###Africa
![Flag Angola](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Angola.svg){width=20px} [Angola](countrypages/Angola.md) - 
![Flag Burkina Faso](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Burkina%20Faso.svg){width=20px} [Burkina Faso](countrypages/Burkina Faso.md) - 
![Flag Burundi](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Burundi.svg){width=20px} [Burundi](countrypages/Burundi.md) - 
![Flag Benin](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Benin.svg){width=20px} [Benin](countrypages/Benin.md) - 
![Flag Botswana](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Botswana.svg){width=20px} [Botswana](countrypages/Botswana.md) - 
![Flag Democratic Republic of the Congo](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Democratic%20Republic%20of%20the%20Congo.svg){width=20px} [Democratic Republic of the Congo](countrypages/Democratic Republic of the Congo.md) - 
![Flag Central African Republic](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Central%20African%20Republic.svg){width=20px} [Central African Republic](countrypages/Central African Republic.md) - 
![Flag Republic of the Congo](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Republic%20of%20the%20Congo.svg){width=20px} [Republic of the Congo](countrypages/Republic of the Congo.md) - 
![Flag Ivory Coast](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20C%C3%B4te%20d%27Ivoire.svg){width=20px} [Ivory Coast](countrypages/Ivory Coast.md) - 
![Flag Cameroon](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Cameroon.svg){width=20px} [Cameroon](countrypages/Cameroon.md) - 
![Flag Cape Verde](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Cape%20Verde.svg){width=20px} [Cape Verde](countrypages/Cape Verde.md) - 
![Flag Djibouti](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Djibouti.svg){width=20px} [Djibouti](countrypages/Djibouti.md) - 
![Flag Algeria](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Algeria.svg){width=20px} [Algeria](countrypages/Algeria.md) - 
![Flag Egypt](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Egypt.svg){width=20px} [Egypt](countrypages/Egypt.md) - 
![Flag Eritrea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Eritrea.svg){width=20px} [Eritrea](countrypages/Eritrea.md) - 
![Flag Ethiopia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Ethiopia.svg){width=20px} [Ethiopia](countrypages/Ethiopia.md) - 
![Flag Gabon](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Gabon.svg){width=20px} [Gabon](countrypages/Gabon.md) - 
![Flag Ghana](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Ghana.svg){width=20px} [Ghana](countrypages/Ghana.md) - 
![Flag The Gambia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20The%20Gambia.svg){width=20px} [The Gambia](countrypages/The Gambia.md) - 
![Flag Guinea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Guinea.svg){width=20px} [Guinea](countrypages/Guinea.md) - 
![Flag Equatorial Guinea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Equatorial%20Guinea.svg){width=20px} [Equatorial Guinea](countrypages/Equatorial Guinea.md) - 
![Flag Guinea-Bissau](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Guinea-Bissau.svg){width=20px} [Guinea-Bissau](countrypages/Guinea-Bissau.md) - 
![Flag Kenya](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kenya.svg){width=20px} [Kenya](countrypages/Kenya.md) - 
![Flag Comoros](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Comoros.svg){width=20px} [Comoros](countrypages/Comoros.md) - 
![Flag Liberia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Liberia.svg){width=20px} [Liberia](countrypages/Liberia.md) - 
![Flag Lesotho](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Lesotho.svg){width=20px} [Lesotho](countrypages/Lesotho.md) - 
![Flag Libya](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Libya.svg){width=20px} [Libya](countrypages/Libya.md) - 
![Flag Morocco](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Morocco.svg){width=20px} [Morocco](countrypages/Morocco.md) - 
![Flag Madagascar](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Madagascar.svg){width=20px} [Madagascar](countrypages/Madagascar.md) - 
![Flag Mali](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mali.svg){width=20px} [Mali](countrypages/Mali.md) - 
![Flag Mauritania](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mauritania.svg){width=20px} [Mauritania](countrypages/Mauritania.md) - 
![Flag Mauritius](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mauritius.svg){width=20px} [Mauritius](countrypages/Mauritius.md) - 
![Flag Malawi](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Malawi.svg){width=20px} [Malawi](countrypages/Malawi.md) - 
![Flag Mozambique](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mozambique.svg){width=20px} [Mozambique](countrypages/Mozambique.md) - 
![Flag Namibia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Namibia.svg){width=20px} [Namibia](countrypages/Namibia.md) - 
![Flag Niger](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Niger.svg){width=20px} [Niger](countrypages/Niger.md) - 
![Flag Nigeria](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Nigeria.svg){width=20px} [Nigeria](countrypages/Nigeria.md) - 
![Flag Rwanda](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Rwanda.svg){width=20px} [Rwanda](countrypages/Rwanda.md) - 
![Flag Seychelles](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Seychelles.svg){width=20px} [Seychelles](countrypages/Seychelles.md) - 
![Flag Sudan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Sudan.svg){width=20px} [Sudan](countrypages/Sudan.md) - 
![Flag Sierra Leone](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Sierra%20Leone.svg){width=20px} [Sierra Leone](countrypages/Sierra Leone.md) - 
![Flag Senegal](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Senegal.svg){width=20px} [Senegal](countrypages/Senegal.md) - 
![Flag Somalia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Somalia.svg){width=20px} [Somalia](countrypages/Somalia.md) - 
![Flag South Sudan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20South%20Sudan.svg){width=20px} [South Sudan](countrypages/South Sudan.md) - 
![Flag São Tomé and Príncipe](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20S%C3%A3o%20Tom%C3%A9%20and%20Pr%C3%ADncipe.svg){width=20px} [São Tomé and Príncipe](countrypages/São Tomé and Príncipe.md) - 
![Flag Eswatini](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Eswatini.svg){width=20px} [Eswatini](countrypages/Eswatini.md) - 
![Flag Chad](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Chad.svg){width=20px} [Chad](countrypages/Chad.md) - 
![Flag Togo](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Togo%20%283-2%29.svg){width=20px} [Togo](countrypages/Togo.md) - 
![Flag Tunisia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Tunisia.svg){width=20px} [Tunisia](countrypages/Tunisia.md) - 
![Flag Tanzania](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Tanzania.svg){width=20px} [Tanzania](countrypages/Tanzania.md) - 
![Flag Uganda](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Uganda.svg){width=20px} [Uganda](countrypages/Uganda.md) - 
![Flag South Africa](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20South%20Africa.svg){width=20px} [South Africa](countrypages/South Africa.md) - 
![Flag Zambia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Zambia.svg){width=20px} [Zambia](countrypages/Zambia.md) - 
![Flag Zimbabwe](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Zimbabwe.svg){width=20px} [Zimbabwe](countrypages/Zimbabwe.md) - 

###Asia
![Flag United Arab Emirates](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20United%20Arab%20Emirates.svg){width=20px} [United Arab Emirates](countrypages/United Arab Emirates.md) - 
![Flag Afghanistan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Taliban.svg){width=20px} [Afghanistan](countrypages/Afghanistan.md) - 
![Flag Armenia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Armenia.svg){width=20px} [Armenia](countrypages/Armenia.md) - 
![Flag Azerbaijan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Azerbaijan.svg){width=20px} [Azerbaijan](countrypages/Azerbaijan.md) - 
![Flag Bangladesh](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bangladesh.svg){width=20px} [Bangladesh](countrypages/Bangladesh.md) - 
![Flag Bahrain](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bahrain.svg){width=20px} [Bahrain](countrypages/Bahrain.md) - 
![Flag Brunei](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Brunei.svg){width=20px} [Brunei](countrypages/Brunei.md) - 
![Flag Bhutan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bhutan.svg){width=20px} [Bhutan](countrypages/Bhutan.md) - 
![Flag People's Republic of China](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20People%27s%20Republic%20of%20China.svg){width=20px} [People's Republic of China](countrypages/People's Republic of China.md) - 
![Flag Indonesia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Indonesia.svg){width=20px} [Indonesia](countrypages/Indonesia.md) - 
![Flag Israel](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Israel.svg){width=20px} [Israel](countrypages/Israel.md) - 
![Flag India](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20India.svg){width=20px} [India](countrypages/India.md) - 
![Flag Iraq](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Iraq.svg){width=20px} [Iraq](countrypages/Iraq.md) - 
![Flag Iran](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Iran.svg){width=20px} [Iran](countrypages/Iran.md) - 
![Flag Jordan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Jordan.svg){width=20px} [Jordan](countrypages/Jordan.md) - 
![Flag Japan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Japan.svg){width=20px} [Japan](countrypages/Japan.md) - 
![Flag Kyrgyzstan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kyrgyzstan.svg){width=20px} [Kyrgyzstan](countrypages/Kyrgyzstan.md) - 
![Flag Cambodia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Cambodia.svg){width=20px} [Cambodia](countrypages/Cambodia.md) - 
![Flag North Korea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20North%20Korea.svg){width=20px} [North Korea](countrypages/North Korea.md) - 
![Flag South Korea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20South%20Korea.svg){width=20px} [South Korea](countrypages/South Korea.md) - 
![Flag Kuwait](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kuwait.svg){width=20px} [Kuwait](countrypages/Kuwait.md) - 
![Flag Kazakhstan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kazakhstan.svg){width=20px} [Kazakhstan](countrypages/Kazakhstan.md) - 
![Flag Laos](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Laos.svg){width=20px} [Laos](countrypages/Laos.md) - 
![Flag Lebanon](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Lebanon.svg){width=20px} [Lebanon](countrypages/Lebanon.md) - 
![Flag Sri Lanka](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Sri%20Lanka.svg){width=20px} [Sri Lanka](countrypages/Sri Lanka.md) - 
![Flag Myanmar](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Myanmar.svg){width=20px} [Myanmar](countrypages/Myanmar.md) - 
![Flag Mongolia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mongolia.svg){width=20px} [Mongolia](countrypages/Mongolia.md) - 
![Flag Maldives](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Maldives.svg){width=20px} [Maldives](countrypages/Maldives.md) - 
![Flag Malaysia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Malaysia.svg){width=20px} [Malaysia](countrypages/Malaysia.md) - 
![Flag Nepal](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Nepal.svg){width=20px} [Nepal](countrypages/Nepal.md) - 
![Flag Oman](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Oman.svg){width=20px} [Oman](countrypages/Oman.md) - 
![Flag Philippines](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Philippines.svg){width=20px} [Philippines](countrypages/Philippines.md) - 
![Flag Pakistan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Pakistan.svg){width=20px} [Pakistan](countrypages/Pakistan.md) - 
![Flag State of Palestine](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Palestine.svg){width=20px} [State of Palestine](countrypages/State of Palestine.md) - 
![Flag Qatar](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Qatar.svg){width=20px} [Qatar](countrypages/Qatar.md) - 
![Flag Saudi Arabia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Saudi%20Arabia.svg){width=20px} [Saudi Arabia](countrypages/Saudi Arabia.md) - 
![Flag Singapore](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Singapore.svg){width=20px} [Singapore](countrypages/Singapore.md) - 
![Flag Syria](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Syria%20%282025-%29%20%28stars%20variant%29.svg){width=20px} [Syria](countrypages/Syria.md) - 
![Flag Thailand](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Thailand.svg){width=20px} [Thailand](countrypages/Thailand.md) - 
![Flag Tajikistan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Tajikistan.svg){width=20px} [Tajikistan](countrypages/Tajikistan.md) - 
![Flag Timor-Leste](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20East%20Timor.svg){width=20px} [Timor-Leste](countrypages/Timor-Leste.md) - 
![Flag Turkmenistan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Turkmenistan.svg){width=20px} [Turkmenistan](countrypages/Turkmenistan.md) - 
![Flag Turkey](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Turkey.svg){width=20px} [Turkey](countrypages/Turkey.md) - 
![Flag Taiwan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Republic%20of%20China.svg){width=20px} [Taiwan](countrypages/Taiwan.md) - 
![Flag Uzbekistan](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Uzbekistan.svg){width=20px} [Uzbekistan](countrypages/Uzbekistan.md) - 
![Flag Vietnam](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Vietnam.svg){width=20px} [Vietnam](countrypages/Vietnam.md) - 
![Flag Yemen](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Yemen.svg){width=20px} [Yemen](countrypages/Yemen.md) - 

###Europe
![Flag Andorra](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Andorra.svg){width=20px} [Andorra](countrypages/Andorra.md) - 
![Flag Albania](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Albania.svg){width=20px} [Albania](countrypages/Albania.md) - 
![Flag Austria](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Austria.svg){width=20px} [Austria](countrypages/Austria.md) - 
![Flag Bosnia and Herzegovina](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bosnia%20and%20Herzegovina.svg){width=20px} [Bosnia and Herzegovina](countrypages/Bosnia and Herzegovina.md) - 
![Flag Belgium](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Belgium.svg){width=20px} [Belgium](countrypages/Belgium.md) - 
![Flag Bulgaria](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bulgaria.svg){width=20px} [Bulgaria](countrypages/Bulgaria.md) - 
![Flag Belarus](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Belarus.svg){width=20px} [Belarus](countrypages/Belarus.md) - 
![Flag Switzerland](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Switzerland.svg){width=20px} [Switzerland](countrypages/Switzerland.md) - 
![Flag Cyprus](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Cyprus.svg){width=20px} [Cyprus](countrypages/Cyprus.md) - 
![Flag Czech Republic](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Czech%20Republic.svg){width=20px} [Czech Republic](countrypages/Czech Republic.md) - 
![Flag Germany](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Germany.svg){width=20px} [Germany](countrypages/Germany.md) - 
![Flag Kingdom of Denmark](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Denmark.svg){width=20px} [Kingdom of Denmark](countrypages/Kingdom of Denmark.md) - 
![Flag Estonia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Estonia.svg){width=20px} [Estonia](countrypages/Estonia.md) - 
![Flag Spain](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Spain.svg){width=20px} [Spain](countrypages/Spain.md) - 
![Flag Finland](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Finland.svg){width=20px} [Finland](countrypages/Finland.md) - 
![Flag France](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20France.svg){width=20px} [France](countrypages/France.md) - 
![Flag United Kingdom](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20United%20Kingdom%20%283-5%29.svg){width=20px} [United Kingdom](countrypages/United Kingdom.md) - 
![Flag Georgia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Georgia.svg){width=20px} [Georgia](countrypages/Georgia.md) - 
![Flag Greece](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Greece.svg){width=20px} [Greece](countrypages/Greece.md) - 
![Flag Croatia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Croatia.svg){width=20px} [Croatia](countrypages/Croatia.md) - 
![Flag Hungary](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Hungary.svg){width=20px} [Hungary](countrypages/Hungary.md) - 
![Flag Ireland](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Ireland.svg){width=20px} [Ireland](countrypages/Ireland.md) - 
![Flag Iceland](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Iceland.svg){width=20px} [Iceland](countrypages/Iceland.md) - 
![Flag Italy](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Italy.svg){width=20px} [Italy](countrypages/Italy.md) - 
![Flag Liechtenstein](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Liechtenstein.svg){width=20px} [Liechtenstein](countrypages/Liechtenstein.md) - 
![Flag Lithuania](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Lithuania.svg){width=20px} [Lithuania](countrypages/Lithuania.md) - 
![Flag Luxembourg](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Luxembourg.svg){width=20px} [Luxembourg](countrypages/Luxembourg.md) - 
![Flag Latvia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Latvia.svg){width=20px} [Latvia](countrypages/Latvia.md) - 
![Flag Monaco](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Monaco.svg){width=20px} [Monaco](countrypages/Monaco.md) - 
![Flag Moldova](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Moldova.svg){width=20px} [Moldova](countrypages/Moldova.md) - 
![Flag Montenegro](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Montenegro.svg){width=20px} [Montenegro](countrypages/Montenegro.md) - 
![Flag North Macedonia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20North%20Macedonia.svg){width=20px} [North Macedonia](countrypages/North Macedonia.md) - 
![Flag Malta](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Malta.svg){width=20px} [Malta](countrypages/Malta.md) - 
![Flag Kingdom of the Netherlands](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Netherlands.svg){width=20px} [Kingdom of the Netherlands](countrypages/Kingdom of the Netherlands.md) - 
![Flag Norway](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Norway.svg){width=20px} [Norway](countrypages/Norway.md) - 
![Flag Poland](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Poland.svg){width=20px} [Poland](countrypages/Poland.md) - 
![Flag Portugal](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Portugal.svg){width=20px} [Portugal](countrypages/Portugal.md) - 
![Flag Romania](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Romania.svg){width=20px} [Romania](countrypages/Romania.md) - 
![Flag Serbia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Serbia.svg){width=20px} [Serbia](countrypages/Serbia.md) - 
![Flag Russia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Russia.svg){width=20px} [Russia](countrypages/Russia.md) - 
![Flag Sweden](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Sweden.svg){width=20px} [Sweden](countrypages/Sweden.md) - 
![Flag Slovenia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Slovenia.svg){width=20px} [Slovenia](countrypages/Slovenia.md) - 
![Flag Slovakia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Slovakia.svg){width=20px} [Slovakia](countrypages/Slovakia.md) - 
![Flag San Marino](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20San%20Marino.svg){width=20px} [San Marino](countrypages/San Marino.md) - 
![Flag Ukraine](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Ukraine.svg){width=20px} [Ukraine](countrypages/Ukraine.md) - 
![Flag Vatican City](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Vatican%20City%20%282023%E2%80%93present%29.svg){width=20px} [Vatican City](countrypages/Vatican City.md) - 

###North America
![Flag Antigua and Barbuda](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Antigua%20and%20Barbuda.svg){width=20px} [Antigua and Barbuda](countrypages/Antigua and Barbuda.md) - 
![Flag Barbados](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Barbados.svg){width=20px} [Barbados](countrypages/Barbados.md) - 
![Flag The Bahamas](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Bahamas.svg){width=20px} [The Bahamas](countrypages/The Bahamas.md) - 
![Flag Belize](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Belize.svg){width=20px} [Belize](countrypages/Belize.md) - 
![Flag Canada](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Canada%20%28Pantone%29.svg){width=20px} [Canada](countrypages/Canada.md) - 
![Flag Costa Rica](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Costa%20Rica.svg){width=20px} [Costa Rica](countrypages/Costa Rica.md) - 
![Flag Cuba](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Cuba.svg){width=20px} [Cuba](countrypages/Cuba.md) - 
![Flag Dominica](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Dominica.svg){width=20px} [Dominica](countrypages/Dominica.md) - 
![Flag Dominican Republic](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Dominican%20Republic.svg){width=20px} [Dominican Republic](countrypages/Dominican Republic.md) - 
![Flag Grenada](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Grenada.svg){width=20px} [Grenada](countrypages/Grenada.md) - 
![Flag Guatemala](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Guatemala.svg){width=20px} [Guatemala](countrypages/Guatemala.md) - 
![Flag Honduras](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Honduras%20%282022-%29.svg){width=20px} [Honduras](countrypages/Honduras.md) - 
![Flag Haiti](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Haiti.svg){width=20px} [Haiti](countrypages/Haiti.md) - 
![Flag Jamaica](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Jamaica.svg){width=20px} [Jamaica](countrypages/Jamaica.md) - 
![Flag Saint Kitts and Nevis](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Saint%20Kitts%20and%20Nevis.svg){width=20px} [Saint Kitts and Nevis](countrypages/Saint Kitts and Nevis.md) - 
![Flag Saint Lucia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Saint%20Lucia.svg){width=20px} [Saint Lucia](countrypages/Saint Lucia.md) - 
![Flag Mexico](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Mexico.svg){width=20px} [Mexico](countrypages/Mexico.md) - 
![Flag Nicaragua](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Nicaragua.svg){width=20px} [Nicaragua](countrypages/Nicaragua.md) - 
![Flag El Salvador](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20El%20Salvador.svg){width=20px} [El Salvador](countrypages/El Salvador.md) - 
![Flag Trinidad and Tobago](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Trinidad%20and%20Tobago.svg){width=20px} [Trinidad and Tobago](countrypages/Trinidad and Tobago.md) - 
![Flag United States](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20United%20States.svg){width=20px} [United States](countrypages/United States.md) - 
![Flag Saint Vincent and the Grenadines](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Saint%20Vincent%20and%20the%20Grenadines.svg){width=20px} [Saint Vincent and the Grenadines](countrypages/Saint Vincent and the Grenadines.md) - 

###Oceania
![Flag Australia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Australia%20%28converted%29.svg){width=20px} [Australia](countrypages/Australia.md) - 
![Flag Fiji](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Fiji.svg){width=20px} [Fiji](countrypages/Fiji.md) - 
![Flag Federated States of Micronesia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Federated%20States%20of%20Micronesia.svg){width=20px} [Federated States of Micronesia](countrypages/Federated States of Micronesia.md) - 
![Flag Kiribati](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Kiribati.svg){width=20px} [Kiribati](countrypages/Kiribati.md) - 
![Flag Marshall Islands](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Marshall%20Islands.svg){width=20px} [Marshall Islands](countrypages/Marshall Islands.md) - 
![Flag Nauru](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Nauru.svg){width=20px} [Nauru](countrypages/Nauru.md) - 
![Flag New Zealand](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20New%20Zealand.svg){width=20px} [New Zealand](countrypages/New Zealand.md) - 
![Flag Papua New Guinea](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Papua%20New%20Guinea.svg){width=20px} [Papua New Guinea](countrypages/Papua New Guinea.md) - 
![Flag Palau](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Palau.svg){width=20px} [Palau](countrypages/Palau.md) - 
![Flag Solomon Islands](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20the%20Solomon%20Islands.svg){width=20px} [Solomon Islands](countrypages/Solomon Islands.md) - 
![Flag Tonga](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Tonga.svg){width=20px} [Tonga](countrypages/Tonga.md) - 
![Flag Tuvalu](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Tuvalu.svg){width=20px} [Tuvalu](countrypages/Tuvalu.md) - 
![Flag Vanuatu](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Vanuatu.svg){width=20px} [Vanuatu](countrypages/Vanuatu.md) - 
![Flag Samoa](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Samoa.svg){width=20px} [Samoa](countrypages/Samoa.md) - 

###South America
![Flag Argentina](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Argentina.svg){width=20px} [Argentina](countrypages/Argentina.md) - 
![Flag Bolivia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Bolivia.svg){width=20px} [Bolivia](countrypages/Bolivia.md) - 
![Flag Brazil](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Brazil.svg){width=20px} [Brazil](countrypages/Brazil.md) - 
![Flag Chile](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Chile.svg){width=20px} [Chile](countrypages/Chile.md) - 
![Flag Colombia](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Colombia.svg){width=20px} [Colombia](countrypages/Colombia.md) - 
![Flag Ecuador](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Ecuador.svg){width=20px} [Ecuador](countrypages/Ecuador.md) - 
![Flag Guyana](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Guyana.svg){width=20px} [Guyana](countrypages/Guyana.md) - 
![Flag Panama](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Panama.svg){width=20px} [Panama](countrypages/Panama.md) - 
![Flag Peru](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Peru.svg){width=20px} [Peru](countrypages/Peru.md) - 
![Flag Paraguay](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Paraguay.svg){width=20px} [Paraguay](countrypages/Paraguay.md) - 
![Flag Suriname](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Suriname.svg){width=20px} [Suriname](countrypages/Suriname.md) - 
![Flag Uruguay](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Uruguay.svg){width=20px} [Uruguay](countrypages/Uruguay.md) - 
![Flag Venezuela](http://commons.wikimedia.org/wiki/Special:FilePath/Flag%20of%20Venezuela.svg){width=20px} [Venezuela](countrypages/Venezuela.md) - 
