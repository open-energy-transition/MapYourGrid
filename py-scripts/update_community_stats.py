import requests
import json
import time
import os
import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# --- CONFIGURATION ---
TEAM_MEMBERS = {
    # Our team usernames here so not picked up as community mappers
    "Andreas Hernandez", "Tobias Augspurger", "Mwiche", "davidtt92", 
    "relaxxe", "Russ", "map-dynartio", "overflorian", "nlehuby", 
    "ben10dynartio", "InfosReseaux"
}
HASHTAG = "mapyourgrid"
STATS_FILE = "docs/data/community-stats.json"
KM_PER_TOWER = 0.317  # Constant for line length estimation

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

    def get_power_tower_counts(self, changesets):
        """Gets the actual power=tower node count for each changeset via Overpass."""
        towers_per_user = defaultdict(int)
        
        # Group changesets by user for efficiency
        changesets_by_user = defaultdict(list)
        for cs in changesets:
            user = cs.get('properties', {}).get('user')
            changeset_id = cs.get('id')
            if user and changeset_id:
                changesets_by_user[user].append(changeset_id)
        
        print(f"Querying Overpass for power=tower counts across {len(changesets_by_user)} users...")
        
        for user, changeset_ids in changesets_by_user.items():
            # Query in batches to avoid timeout
            batch_size = 50
            user_tower_count = 0
            
            for i in range(0, len(changeset_ids), batch_size):
                batch = changeset_ids[i:i + batch_size]
                changeset_filter = "".join(f"(changed:\"{cs_id}\");" for cs_id in batch)
                
                query = f"""
                [out:json][timeout:180];
                (
                  node["power"="tower"](user:"{user}"){changeset_filter}
                );
                out count;
                """
                
                try:
                    response = requests.post(self.overpass_base, data={"data": query}, timeout=200)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Extract count from Overpass response
                    count = data.get('elements', [{}])[0].get('tags', {}).get('total', 0)
                    user_tower_count += count
                    
                    time.sleep(2)  # Be respectful to Overpass API
                    
                except requests.RequestException as e:
                    print(f"Warning: Overpass query failed for user {user}, batch {i//batch_size + 1}: {e}")
                    continue
            
            towers_per_user[user] = user_tower_count
            print(f"  {user}: {user_tower_count} towers")
        
        return towers_per_user

    def calculate_community_stats(self, changesets):
        """Separates users and calculates tower counts for the community."""
        towers_per_user = self.get_power_tower_counts(changesets)
        
        community_users = {u: c for u, c in towers_per_user.items() if u not in TEAM_MEMBERS}
        community_tower_count = sum(community_users.values())
        
        print(f"Identified {len(community_users)} community mappers.")
        print(f"Total new towers from community: {community_tower_count}")
        return community_users, community_tower_count

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
    else: # weekly mode. Set to 2 days, but then will be updated to 7 days
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
        
        # Calculate line length using the constant
        new_line_length = round(new_tower_count * KM_PER_TOWER)
        print(f"Calculated line length: {new_line_length} km ({new_tower_count} towers × {KM_PER_TOWER})")

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