import requests
import json
import re
from datetime import datetime
import sys
import time

def convert_to_mw(value):
    """
    Converts a power capacity string (e.g., "100 MW", "500 kW", "1 GW") to megawatts.
    """
    if not value:
        return 0

    val_str = str(value).strip().lower()
    
    # Improved regex to handle various formats
    match = re.search(r'(\d+(\.\d+)?)\s*(gw|mw|kw)?', val_str)
    
    if not match:
        return 0

    num = float(match.group(1))
    unit = match.group(3)

    if unit == 'gw':
        return num * 1000
    if unit == 'kw':
        return num / 1000
    
    # Assume MW if no unit is specified
    return num

def fetch_power_plant_capacity():
    """
    Fetches power plant data from the Overpass API and calculates total capacity.
    """
    print("Starting Overpass API request...")
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    query = """
    [out:json][timeout:900];
                
    nwr["power"="plant"](user_touched:"Andreas Hernandez","Tobias Augspurger","davidtt92","Mwiche","relaxxe")->.plants;
    nwr["power"="plant"](user: "Russ","map-dynartio","overflorian","nlehuby","ben10dynartio","InfosReseaux")(newer:"2025-03-01T00:00:00Z")->.more_plants;


    (
     .plants;
     .more_plants;
        );

    out body;
    >;
    out skel qt;
    """

    try:
        print("Sending request to Overpass API...")
        print("This may take several minutes for large datasets...")
        
        # Add explicit timeout for requests (10 minutes max)
        response = requests.post(
            overpass_url, 
            data={"data": query},
            timeout=600  # 10 minutes timeout
        )
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response text: {response.text[:1000]}")
            return None
        
        response.raise_for_status()
        
        print("Parsing JSON response...")
        data = response.json()
        
        print(f"Received {len(data.get('elements', []))} elements from API")
        
        total_capacity_mw = 0
        plant_count = 0

        for element in data.get("elements", []):
            if "tags" in element and "plant:output:electricity" in element["tags"]:
                capacity_str = element["tags"]["plant:output:electricity"]
                capacity_mw = convert_to_mw(capacity_str)
                if capacity_mw > 0:
                    total_capacity_mw += capacity_mw
                    plant_count += 1
        
        print(f"Processed {plant_count} plants with total capacity {total_capacity_mw} MW")
        
        return {
            "total_capacity_mw": round(total_capacity_mw, 2),
            "plant_count": plant_count,
            "updated": datetime.utcnow().isoformat()
        }

    except requests.exceptions.Timeout:
        print("ERROR: Request timed out after 10 minutes")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode error: {e}")
        print(f"Response content (first 1000 chars): {response.text[:1000]}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None

def fetch_substation_count():
    """
    Fetches substation data from the Overpass API and counts total substations.
    """
    print("Starting Overpass API request for substations...")
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    query = """
    [out:json][timeout:1300];
                
    nwr["power"="substation"](user_touched:"Andreas Hernandez","Tobias Augspurger","davidtt92","Mwiche","relaxxe")->.subs;
    nwr["power"="substation"](user:"Russ","map-dynartio","overflorian","nlehuby","ben10dynartio","InfosReseaux")(newer:"2025-03-01T00:00:00Z")->.more_subs;

    (
     .subs;
     .more_subs;
        );

    out count;
    """

    try:
        print("Sending request to Overpass API for substations...")
        headers = {
            'User-Agent': 'MapYourGrid Line Length Script (via GitHub Action; +https://github.com/open-energy-transition/MapYourGrid)'
        }

        response = requests.post(
            overpass_url, 
            data={"data": query},
            headers = headers,
            timeout=1320  # 10 minutes timeout
        )
        
        print(f"Substations response status code: {response.status_code}")
        print(f"Substations response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response text: {response.text[:1000]}")
            return None
        
        response.raise_for_status()
        
        print("Parsing JSON response for substations...")
        data = response.json()
        
        print(f"Received substation count data from API")
        
        # Extract count from the response
        elements = data.get("elements", [])
        if not elements:
            print("ERROR: Substation count query returned no elements.")
            print("–– raw Overpass JSON (first 2000 chars) ––")
            print(json.dumps(data, indent=2)[:2000])
            return None
            
        count_tags = elements[0].get("tags", {})
        substation_count = int(count_tags.get("total", 0))
        
        print(f"Total substations: {substation_count}")
        
        return {
            "substation_count": substation_count
        }
    
    except requests.exceptions.Timeout:
        print("ERROR: Substations request timed out after 10 minutes")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"ERROR: Substations connection error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Substations request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Substations JSON decode error: {e}")
        print(f"Response content (first 1000 chars): {response.text[:1000]}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected substations error: {e}")
        import traceback
        traceback.print_exc()
        return None

def fetch_power_data():
    """
    Fetches both power plant and substation data and combines them.
    """
    print("Fetching power infrastructure data...")
    
    # Fetch power plant data
    plant_data = fetch_power_plant_capacity()
    if not plant_data:
        print("ERROR: Failed to fetch power plant data")
        return None
    
    print("Pausing for 20 seconds before next request...")
    time.sleep(30) 
    
    
    # Fetch substation data
    substation_data = fetch_substation_count()
    if not substation_data:
        print("ERROR: Failed to fetch substation data")
        return None
    
    # Combine the data
    combined_data = {
        "total_capacity_mw": plant_data["total_capacity_mw"],
        "plant_count": plant_data["plant_count"],
        "substation_count": substation_data["substation_count"],
        "updated": datetime.utcnow().isoformat()
    }
    
    return combined_data

if __name__ == "__main__":
    print("Script starting...")
    print(f"Python version: {sys.version}")
    
    power_data = fetch_power_data()
    print(f"Power data result: {power_data}")

    
    if power_data:
        # Ensure the data directory exists
        import os
        print("Creating docs/data directory...")
        os.makedirs("docs/data", exist_ok=True)
        
        print("Writing JSON file...")
        with open("docs/data/power-stats.json", "w") as f:
            json.dump(power_data, f, indent=2)
        
        print("Successfully updated power infrastructure data.")
        print(f"Total Capacity: {power_data['total_capacity_mw']} MW")
        print(f"Plant Count: {power_data['plant_count']}")
        print(f"Substation Count: {power_data['substation_count']}")
    else:
        print("ERROR: No power data returned - check the logs above for errors")
        sys.exit(1)  # Exit with error code so GitHub Actions shows failure