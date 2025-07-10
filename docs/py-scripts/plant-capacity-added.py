import requests
import json
import re
from datetime import datetime

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
    
    query = f"""
    [out:json][timeout:900];
                
    nwr["power"="plant"](user_touched:"Andreas Hernandez","Tobias Augspurger","davidtt92","Mwiche","relaxxe")->.plants;
    nwr["power"="plant"](user_touched: "Russ","map-dynartio","overflorian","nlehuby","ben10dynartio","InfosReseaux")(newer:"2025-03-01T00:00:00Z")->.their_plants;

    (
     .plants;
     .their_plants;
        );

    out body;
    >;
    out skel qt;
    """

    try:
        print("Sending request to Overpass API...")
        response = requests.post(overpass_url, data={"data": query})
        print(f"Response status code: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        print(f"Received {len(data.get('elements', []))} elements from API")
        
        response = requests.post(overpass_url, data={"data": query})
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        total_capacity_mw = 0
        plant_count = 0

        for element in data.get("elements", []):
            if "tags" in element and "plant:output:electricity" in element["tags"]:
                capacity_str = element["tags"]["plant:output:electricity"]
                capacity_mw = convert_to_mw(capacity_str)
                if capacity_mw > 0:
                    total_capacity_mw += capacity_mw
                    plant_count += 1
        
        return {
            "total_capacity_mw": round(total_capacity_mw, 2),
            "plant_count": plant_count,
            "updated": datetime.utcnow().isoformat()
        }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    capacity_data = fetch_power_plant_capacity()
    if capacity_data:
        # Ensure the data directory exists
        import os
        os.makedirs("docs/data", exist_ok=True)
        
        with open("docs/data/plant-capacity.json", "w") as f:
            json.dump(capacity_data, f, indent=2)
        
        print("Successfully updated plant capacity data.")
        print(f"Total Capacity: {capacity_data['total_capacity_mw']} MW")
        print(f"Plant Count: {capacity_data['plant_count']}")