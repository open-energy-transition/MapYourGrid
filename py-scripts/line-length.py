import requests
import json
import math
import os
import html
import re
import time
from datetime import datetime, timezone
from bs4 import BeautifulSoup

# --- Configuration ---
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OPENINFRAMAP_URL = "https://openinframap.org/stats"
OUTPUT_DIR = "docs/data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "line-length.json")

# Overpass QL query to fetch the relevant power line data
OVERPASS_QUERY = """
[out:json][timeout:900];
node["power"="pole"](user_touched:"Andreas Hernandez","Tobias Augspurger","davidtt92","Mwiche","relaxxe") -> .poles;
node["power"="tower"](user_touched:"Andreas Hernandez","Tobias Augspurger","davidtt92","Mwiche","relaxxe") -> .towers;
node["power"="pole"](user:"Russ","map-dynartio","overflorian","nlehuby","ben10dynartio","InfosReseaux")(newer:"2025-03-01T00:00:00Z")->.their_poles;
node["power"="tower"](user:"Russ","map-dynartio","overflorian","nlehuby","ben10dynartio","InfosReseaux")(newer:"2025-03-01T00:00:00Z")->.their_towers;

(node.towers; node.poles;) -> .supports;
(node.their_towers; node.their_poles;) -> .their_supports;

way["power"="line"](bn.supports)-> .connected_ways;
way["power"="line"](bn.their_supports)-> .theirconnected_ways;

(.poles; .towers; .connected_ways; .theirconnected_ways; .their_poles; .their_towers;);
out body;
>;
out skel qt;
"""

# --- Helper Functions ---

def retry_request(func, max_retries=4, delay=10):
    """Simple retry wrapper with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except ConnectionError as e:
            print(f"Unable to connect to Overpass: {e}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"Timeout when querying Overpass: {e}")
            return None
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            if attempt == max_retries - 1:
                raise
            wait_time = delay * (2 ** attempt)
            print(f"Attempt {attempt + 1} failed: {e} ({e.response.text if e.response is not None else 'No answer'}). Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Undefined error fetching from Overpass: {e}")
            return None


def haversine_distance(coord1, coord2):
    """Calculates the distance between two lat/lon coordinates in kilometers."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_line_stats():
    """Fetches and calculates line length stats from Overpass API."""
    print("Fetching data from Overpass API...")
    
    def _fetch_overpass():
        headers = {
            'User-Agent': 'MapYourGrid Line Length Script (via GitHub Action; +https://github.com/open-energy-transition/MapYourGrid)'
        }
        response = requests.post(OVERPASS_URL, data={'data': OVERPASS_QUERY}, headers=headers,
            timeout=1100)
        response.raise_for_status()
        data = response.json()
        # Overpass sometimes answer errors with HTTP 200 code that won't trigger exception
        if not data:
            print(f"Invalid response from Overpass: {response}")
        return data
    
    data = retry_request(_fetch_overpass)
    if not data:
        return None
    
    nodes = {el['id']: (el['lat'], el['lon'])
             for el in data.get('elements', [])
             if el.get('type') == 'node' and el.get('tags', {}).get('power') in ['tower', 'pole']}
    
    ways = [el for el in data.get('elements', []) if el.get('type') == 'way' and el.get('tags', {}).get('power') == 'line']

    total_length = 0
    way_count = 0
    for way in ways:
        way_nodes = [node_id for node_id in way.get('nodes', []) if node_id in nodes]
        if len(way_nodes) >= 2:
            way_count += 1
            coords = [nodes[node_id] for node_id in way_nodes]
            for i in range(len(coords) - 1):
                total_length += haversine_distance(coords[i], coords[i+1])
    
    print(f"Team contribution: {round(total_length)} km from {way_count} ways and {len(nodes)} nodes.")
    return {
        "lengthKm": round(total_length),
        "wayCount": way_count,
        "towerCount": len(nodes)
    }

def clean_voltage(voltage_text):
    """Decode HTML entities and normalize spaces/dashes."""
    text = html.unescape(voltage_text)
    text = text.replace('\xa0', ' ')  # non-breaking space
    text = text.replace('–', '-')     # en dash to hyphen
    return text.strip()

def parse_km(length_str):
    """Extract km number from a string like '1,234 km'."""
    match = re.search(r'([\d,\s]+)\s*km', length_str)
    if not match:
        return None
    cleaned = match.group(1).replace(',', '').replace(' ', '')
    try:
        return int(cleaned)
    except ValueError:
        return None
    
def get_global_stats():
    """Scrapes and parses global stats from OpenInfraMap, excluding low voltage ranges."""
    print("Fetching OpenInfraMap global stats...")
    try:
        response = requests.get(OPENINFRAMAP_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not fetch OpenInfraMap stats. {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    total_km = 0
    excluded_low_voltage_km = 0
    low_voltage_ranges = ['0 V - 9 kV', '10 kV - 24 kV', '25 kV - 51 kV']

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 2:
            continue

        voltage = clean_voltage(cols[0].text)
        length_str = clean_voltage(cols[1].text)

        km = parse_km(length_str)
        if km is None:
            continue

        if 'total' in voltage.lower():
            total_km = km
        elif voltage in low_voltage_ranges:
            excluded_low_voltage_km += km

    if total_km > 0:
        medium_high_total = total_km - excluded_low_voltage_km
        print(f"Global total: {total_km} km")
        print(f"Excluded low voltage: {excluded_low_voltage_km} km")
        print(f"Global medium-high voltage total: {medium_high_total} km")
        return {
            "totalGlobalKm": total_km,
            "mediumHighVoltageKm": medium_high_total
        }
    
    print("Warning: Could not parse global stats from HTML.")
    return None

# --- Main Execution ---
if __name__ == "__main__":
    line_stats = get_line_stats()
    
    if not line_stats:
        exit(1) # Exit if Overpass data failed

    time.sleep(5)
    global_stats = get_global_stats()

    # Combine results into the final JSON structure
    final_data = {
        "lengthKm": line_stats["lengthKm"],
        "totalGlobalKm": None,
        "mediumHighVoltageKm": None,
        "percentageOfMediumHigh": None,
        "towerCount": line_stats["towerCount"],
        "updated": datetime.now(timezone.utc).isoformat()
    }
    
    if global_stats and global_stats["mediumHighVoltageKm"] > 0:
        final_data.update(global_stats)
        percentage = (line_stats["lengthKm"] * 100) / global_stats["mediumHighVoltageKm"]
        final_data["percentageOfMediumHigh"] = round(percentage, 2)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Write the final JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_data, f, indent=2)
    
    print(f"Successfully created {OUTPUT_FILE}")
    print(json.dumps(final_data, indent=2))