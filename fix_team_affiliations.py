#!/usr/bin/env python3
"""
Extract team affiliations from research markdown files and update JSON data files.
"""

import json
import re
import os
from pathlib import Path
from collections import defaultdict

# City name mapping (research file prefix -> JSON file name)
CITY_MAPPING = {
    'atlanta': 'atlanta',
    'austin': 'austin',
    'boston': 'boston',
    'chicago': 'chicago',
    'cleveland': 'cleveland',
    'dallas': 'dallas',
    'denver': 'denver',
    'detroit': 'detroit',
    'houston': 'houston',
    'vegas': 'las-vegas',
    'miami': 'miami',
    'minneapolis': 'minneapolis',
    'nyc': 'nyc',  # Note: both nyc.json and new-york-city.json exist
    'oc': 'orange-county',
    'philadelphia': 'philadelphia',
    'phoenix': 'phoenix',
    'pittsburgh': 'pittsburgh',
    'san-diego': 'san-diego',
    'seattle': 'seattle',
    'sf-bay': 'sf-bay-area'
}

# Sport type mapping from file names
SPORT_FILES = {
    'nfl': 'NFL',
    'mlb': 'MLB',
    'nba': 'NBA',
    'nhl': 'NHL'
}


def normalize_venue_name(name):
    """Normalize venue name for matching."""
    # Remove possessives, punctuation, extra spaces
    name = name.lower()
    name = re.sub(r"'s\b", '', name)  # Remove 's
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name)  # Normalize spaces
    return name.strip()


def parse_research_file(filepath):
    """
    Parse a research markdown file and extract venue -> team mappings.
    
    Format 1 (most files):
    ## Team Name
    ### Venue Name
    - Address: ...
    
    Format 2 (boston, etc):
    ## Team Name (HOME TEAM)
    - **Bar Name**: Venue Name
    - **Address**: ...
    
    Returns: dict of {normalized_venue_name: team_name}
    """
    venue_teams = {}
    current_team = None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for line in lines:
            # Match team header (## Team Name or ## Team Name (HOME TEAM))
            team_match = re.match(r'^##\s+(.+?)(?:\s+\(HOME TEAM\))?$', line)
            if team_match:
                current_team = team_match.group(1).strip()
                continue
            
            # Format 1: Match venue header (### Venue Name)
            venue_match = re.match(r'^###\s+(.+)$', line)
            if venue_match and current_team:
                venue_name = venue_match.group(1).strip()
                normalized = normalize_venue_name(venue_name)
                
                if normalized:  # Only add if we got a valid name
                    if normalized not in venue_teams:
                        venue_teams[normalized] = []
                    if current_team not in venue_teams[normalized]:
                        venue_teams[normalized].append(current_team)
                continue
            
            # Format 2: Match - **Bar Name**: Venue Name
            bar_name_match = re.match(r'^-\s+\*\*Bar Name\*\*:\s+(.+)$', line)
            if bar_name_match and current_team:
                venue_name = bar_name_match.group(1).strip()
                normalized = normalize_venue_name(venue_name)
                
                if normalized:  # Only add if we got a valid name
                    if normalized not in venue_teams:
                        venue_teams[normalized] = []
                    if current_team not in venue_teams[normalized]:
                        venue_teams[normalized].append(current_team)
        
        return venue_teams
    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return {}


def build_team_mapping():
    """
    Build complete mapping of venue names to teams from all research files.
    
    Returns: dict of {city: {normalized_venue_name: [teams]}}
    """
    research_dir = Path('/data/.openclaw/workspace/research')
    city_mappings = defaultdict(lambda: defaultdict(list))
    
    # Process all sport-specific research files
    for research_file in research_dir.glob('*.md'):
        filename = research_file.name
        
        # Parse filename: city-sport-bars.md
        parts = filename.replace('.md', '').split('-')
        
        # Identify sport type
        sport = None
        city_prefix = None
        
        for sport_key in SPORT_FILES.keys():
            if sport_key in parts:
                sport = sport_key
                # Get city prefix (everything before sport)
                sport_idx = parts.index(sport_key)
                city_prefix = '-'.join(parts[:sport_idx])
                break
        
        # Skip if not a sport-specific file or unknown city
        if not sport or not city_prefix:
            continue
        
        if city_prefix not in CITY_MAPPING:
            print(f"Warning: Unknown city prefix '{city_prefix}' in {filename}")
            continue
        
        city_json_name = CITY_MAPPING[city_prefix]
        
        print(f"Processing {filename} -> {city_json_name} ({SPORT_FILES[sport]})")
        
        # Parse the file
        venue_teams = parse_research_file(research_file)
        
        # Add to city mapping
        for venue_norm, teams in venue_teams.items():
            for team in teams:
                if team not in city_mappings[city_json_name][venue_norm]:
                    city_mappings[city_json_name][venue_norm].append(team)
        
        print(f"  Found {len(venue_teams)} venues with team affiliations")
    
    return city_mappings


def update_json_files(city_mappings):
    """
    Update JSON files with team affiliations from the mapping.
    """
    data_dir = Path('/data/.openclaw/workspace/where-to-watch-the-game/data')
    stats = {
        'cities_processed': 0,
        'venues_updated': 0,
        'teams_added': 0,
        'venues_total': 0
    }
    
    for json_file in data_dir.glob('*.json'):
        # Skip the master file
        if json_file.name == 'ALL_CITIES_MASTER.json':
            continue
        
        city_name = json_file.stem
        
        # Skip if we don't have mappings for this city
        if city_name not in city_mappings:
            print(f"No team mapping for {city_name}, skipping...")
            continue
        
        print(f"\nUpdating {json_file.name}...")
        
        # Load JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        city_stats = {'updated': 0, 'teams': 0}
        venue_mapping = city_mappings[city_name]
        
        # Update each venue
        for venue in data.get('venues', []):
            stats['venues_total'] += 1
            venue_name = venue.get('name', '')
            normalized = normalize_venue_name(venue_name)
            
            if normalized in venue_mapping:
                teams = venue_mapping[normalized]
                # Only update if currently empty or different
                if not venue.get('team_affiliations') or venue['team_affiliations'] != teams:
                    venue['team_affiliations'] = teams
                    city_stats['updated'] += 1
                    city_stats['teams'] += len(teams)
        
        # Save updated JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        stats['cities_processed'] += 1
        stats['venues_updated'] += city_stats['updated']
        stats['teams_added'] += city_stats['teams']
        
        print(f"  Updated {city_stats['updated']} venues with {city_stats['teams']} team affiliations")
    
    return stats


def main():
    print("=" * 60)
    print("TEAM AFFILIATION EXTRACTION & UPDATE")
    print("=" * 60)
    print()
    
    # Step 1: Build team mapping from research files
    print("Step 1: Parsing research files...")
    print("-" * 60)
    city_mappings = build_team_mapping()
    
    print()
    print(f"Completed! Found mappings for {len(city_mappings)} cities")
    
    # Show summary
    total_venues = sum(len(venues) for venues in city_mappings.values())
    total_teams = sum(len(teams) for venues in city_mappings.values() 
                     for teams in venues.values())
    print(f"Total venues with teams: {total_venues}")
    print(f"Total team-venue pairs: {total_teams}")
    
    # Step 2: Update JSON files
    print()
    print("Step 2: Updating JSON files...")
    print("-" * 60)
    stats = update_json_files(city_mappings)
    
    # Final report
    print()
    print("=" * 60)
    print("FINAL STATISTICS")
    print("=" * 60)
    print(f"Cities processed: {stats['cities_processed']}")
    print(f"Total venues in JSON files: {stats['venues_total']}")
    print(f"Venues updated with teams: {stats['venues_updated']}")
    print(f"Team affiliations added: {stats['teams_added']}")
    print()
    
    if stats['venues_updated'] > 0:
        print("✅ SUCCESS! Team affiliations have been extracted and updated.")
    else:
        print("⚠️  WARNING: No venues were updated. Check data alignment.")
    
    return stats


if __name__ == '__main__':
    main()
