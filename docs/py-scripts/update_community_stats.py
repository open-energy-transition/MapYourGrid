import requests
import json
import asyncio
import aiohttp
import time
import math
import os
import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# --- CONFIGURATION ---
TEAM_MEMBERS = {
    # Add all your core team usernames here
    "Andreas Hernandez", "Tobias Augspurger", "Mwiche", "davidtt92", 
    "relaxxe", "Russ", "map-dynartio", "overflorian", "nlehuby", 
    "ben10dynartio", "InfosReseaux"
}
HASHTAG = "ohmygrid"
STATS_FILE = "docs/data/community-stats.json"

class CommunityStatsAnalyzer:
    def __init__(self, osmcha_token):
        self.osmcha_base = "https://osmcha.org/api/v1"
        self.overpass_base = "https://overpass-api.de/api/interpreter"
        self.headers = {'Authorization': f'Token {osmcha_token}'}
        print("Community Stats Analyzer initialized.")

    def get_changesets_by_hashtag(self, start_date, end_date):
        """Fetches all changesets for the hashtag within a date range."""
        url = f"{self.osmcha_base}/changesets/"
        params = {'comment': f'#{HASHTAG}', 'page_size': 100, 'order_by': 'date'}
        if start_date: params['date__gte'] = start_date
        if end_date: params['date__lte'] = end_date

        all_changesets = []
        page = 1
        while True:
            params['page'] = page
            try:
                print(f"Fetching page {page} of changesets from OSMCha...")
                response = requests.get(url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                features = data.get('features', [])
                if not features: break
                all_changesets.extend(features)
                if not data.get('next'): break
                page += 1
                time.sleep(1) # Be respectful to the API
            except requests.RequestException as e:
                raise RuntimeError(f"OSMCha fetch failed: {e}")
        print(f"Found {len(all_changesets)} changesets in the specified period.")
        return all_changesets

    def calculate_community_stats(self, changesets):
        """Separates users and calculates tower counts for the community."""
        towers_per_user = defaultdict(int)
        for cs in changesets:
            user = cs.get('properties', {}).get('user')
            create_count = cs.get('properties', {}).get('create', 0)
            if user:
                towers_per_user[user] += create_count
        
        community_users = {u: c for u, c in towers_per_user.items() if u not in TEAM_MEMBERS}
        community_tower_count = sum(community_users.values())
        
        print(f"Identified {len(community_users)} community mappers.")
        print(f"Total new towers from community: {community_tower_count}")
        return community_users, community_tower_count

    def get_community_line_length(self, community_users):
        """Builds and runs an Overpass query to get line length for community users."""
        if not community_users:
            print("No community users found, skipping line length calculation.")
            return None

        user_query_part = ", ".join(f'"{user}"' for user in community_users)
        query = f"""
        [out:json][timeout:900];
        node["power"="tower"](user:{user_query_part})->.community_towers;
        way["power"="line"](bn.community_towers)->.connected_ways;
        (
          node.community_towers;
          way.connected_ways;
        );
        out body;
        >;
        out skel qt;
        """
        
        print("Running Overpass query for line length... (this may take a while)")
        try:
            response = requests.post(self.overpass_base, data={"data": query})
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error querying Overpass API: {e}")
            return None

        print("Calculating distance from Overpass data...")
        return self._calculate_haversine_distance(data)

    def _calculate_haversine_distance(self, data):
        """Calculates total line length in km from Overpass JSON data."""
        nodes = { el['id']: (el['lat'], el['lon']) for el in data['elements'] if el['type'] == 'node' and el.get('tags', {}).get('power') == 'tower' }
        total_length_km = 0

        for el in data['elements']:
            if el['type'] == 'way' and 'nodes' in el:
                way_nodes = el['nodes']
                for i in range(len(way_nodes) - 1):
                    node1_id, node2_id = way_nodes[i], way_nodes[i+1]
                    if node1_id in nodes and node2_id in nodes:
                        coord1, coord2 = nodes[node1_id], nodes[node2_id]
                        
                        lat1, lon1 = coord1
                        lat2, lon2 = coord2
                        R = 6371 # Earth radius in km
                        dLat = math.radians(lat2 - lat1)
                        dLon = math.radians(lon2 - lon1)
                        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
                             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                             math.sin(dLon / 2) * math.sin(dLon / 2))
                        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                        total_length_km += R * c
        
        print(f"Calculated total line length: {round(total_length_km)} km")
        return round(total_length_km)

def main(mode, start_date_str):
    # We need the OSMCha token from environment variables in GitHub Actions
    osmcha_token = os.getenv('OSMCHA_TOKEN')
    if not osmcha_token:
        raise ValueError("OSMCHA_TOKEN environment variable not set!")

    analyzer = CommunityStatsAnalyzer(osmcha_token)

    end_date = datetime.utcnow()
    if mode == 'initial':
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        # Initialize stats from scratch
        previous_stats = {
            "towerCount": 0,
            "lengthKm": 0,
            "users": {},
            "updated": ""
        }
    else: # weekly mode
        start_date = end_date - timedelta(days=7)
        # Load previous stats to update them
        try:
            with open(STATS_FILE, 'r') as f:
                previous_stats = json.load(f)
            print(f"Loaded previous stats from {STATS_FILE}")
        except FileNotFoundError:
            print("Warning: Stats file not found. Starting from zero.")
            previous_stats = {"towerCount": 0, "lengthKm": 0, "users": {}}

    # Fetch changesets from the last week (or initial period)
    try:
        changesets = analyzer.get_changesets_by_hashtag(
        start_date.strftime("%Y-%m-%d"), 
        end_date.strftime("%Y-%m-%d")
    )
    # Calculate stats for the new period
        community_users, new_tower_count = analyzer.calculate_community_stats(changesets)
        new_line_length = analyzer.get_community_line_length(community_users.keys())
    
        if new_line_length is None:
            raise RuntimeError("Line-length calculation failed")
    except Exception as e:
        print(f"[ERROR] Aborting update: {e}")
        sys.exit(1)
    
    # Combine new stats with previous stats
    final_stats = {
        "towerCount": previous_stats.get("towerCount", 0) + new_tower_count,
        "lengthKm": previous_stats.get("lengthKm", 0) + new_line_length,
        "users": previous_stats.get("users", {}),
        "updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    # Update user-specific counts
    for user, count in community_users.items():
        final_stats["users"][user] = final_stats["users"].get(user, 0) + count
        
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(final_stats, f, indent=2)

    print(f"\n✅ Successfully updated community stats in {STATS_FILE}")
    print(f"Total Towers: {final_stats['towerCount']}")
    print(f"Total Line Length: {final_stats['lengthKm']} km")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update MapYourGrid community stats.")
    parser.add_argument(
        '--mode', 
        type=str, 
        choices=['initial', 'weekly'], 
        default='weekly', 
        help="Run mode: 'initial' for a full historical run, 'weekly' for an incremental update."
    )
    parser.add_argument(
        '--start-date',
        type=str,
        default='2025-03-01',
        help="The start date for the initial run (YYYY-MM-DD)."
    )
    args = parser.parse_args()
    
    main(args.mode, args.start_date)