#!/usr/bin/env python3
"""
Convert all city research data to JSON format
Processes markdown files from /data/.openclaw/workspace/research/
Handles both formats: ### Venue and - **Bar Name**:
"""

import json
import re
import os
from pathlib import Path

# Cities to process (the 13 new ones)
NEW_CITIES = [
    'houston', 'philadelphia', 'san-diego', 'dallas', 'boston',
    'detroit', 'minneapolis', 'sf-bay', 'seattle', 'miami',
    'atlanta', 'cleveland', 'pittsburgh'
]

RESEARCH_DIR = Path('/data/.openclaw/workspace/research')
OUTPUT_DIR = Path('/data/.openclaw/workspace/where-to-watch-the-game/data')

def parse_markdown_file(filepath):
    """Parse a markdown file and extract venues - handles both formats"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    current_team = "All Teams"
    teams = {}
    current_venue = None
    
    lines = content.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Team headers (## Something but not ###)
        if line_stripped.startswith('## ') and not line_stripped.startswith('###'):
            current_team = line_stripped.replace('##', '').strip()
            # Clean up team name
            if '(' in current_team:
                current_team = current_team.split('(')[0].strip()
            if current_team not in teams:
                teams[current_team] = []
            # Save previous venue when switching teams
            if current_venue and current_venue.get('name'):
                if current_team not in teams:
                    teams[current_team] = []
                teams[current_team].append(current_venue)
                current_venue = None
            continue
        
        # FORMAT 1: ### Venue Name (Detroit format)
        if line_stripped.startswith('### '):
            # Save previous venue
            if current_venue and current_venue.get('name'):
                if current_team not in teams:
                    teams[current_team] = []
                teams[current_team].append(current_venue)
            
            # Start new venue
            name = line_stripped.replace('###', '').strip()
            current_venue = {
                'name': name,
                'address': '',
                'description': '',
                'phone': '',
                'website': '',
                'hours': ''
            }
            continue
        
        # FORMAT 2: - **Bar Name**: (Houston format)
        if line_stripped.startswith('- **Bar Name**:') or line_stripped.startswith('**Bar Name**:'):
            # Save previous venue
            if current_venue and current_venue.get('name'):
                if current_team not in teams:
                    teams[current_team] = []
                teams[current_team].append(current_venue)
            
            # Start new venue
            name = line_stripped.replace('- **Bar Name**:', '').replace('**Bar Name**:', '').strip()
            current_venue = {
                'name': name,
                'address': '',
                'description': '',
                'phone': '',
                'website': '',
                'hours': ''
            }
            continue
        
        # Parse venue fields (both formats use - **Field**:)
        if current_venue and line_stripped:
            if line_stripped.startswith('- **Address**:') or line_stripped.startswith('**Address**:'):
                current_venue['address'] = line_stripped.replace('- **Address**:', '').replace('**Address**:', '').strip()
            elif line_stripped.startswith('- **Phone**:') or line_stripped.startswith('**Phone**:'):
                current_venue['phone'] = line_stripped.replace('- **Phone**:', '').replace('**Phone**:', '').strip()
            elif line_stripped.startswith('- **Website**:') or line_stripped.startswith('**Website**:'):
                current_venue['website'] = line_stripped.replace('- **Website**:', '').replace('**Website**:', '').strip()
            elif line_stripped.startswith('- **Hours**:') or line_stripped.startswith('**Hours**:'):
                current_venue['hours'] = line_stripped.replace('- **Hours**:', '').replace('**Hours**:', '').strip()
            elif line_stripped.startswith('- **Notes**:') or line_stripped.startswith('**Notes**:'):
                current_venue['description'] = line_stripped.replace('- **Notes**:', '').replace('**Notes**:', '').strip()
    
    # Don't forget the last venue
    if current_venue and current_venue.get('name'):
        if current_team not in teams:
            teams[current_team] = []
        teams[current_team].append(current_venue)
    
    return teams

def process_city(city_name):
    """Process all sports files for a city"""
    city_data = {
        'NFL': {},
        'MLB': {},
        'NBA': {},
        'NHL': {}
    }
    
    leagues = ['nfl', 'mlb', 'nba', 'nhl']
    
    for league in leagues:
        filename = f"{city_name}-{league}-bars.md"
        filepath = RESEARCH_DIR / filename
        
        if filepath.exists():
            print(f"  Processing {league.upper()} from {filename}")
            teams = parse_markdown_file(filepath)
            city_data[league.upper()] = teams
        else:
            print(f"  Skipping {league.upper()} - file not found: {filename}")
    
    return city_data

def get_total_venues(city_data):
    """Count total venues across all sports"""
    total = 0
    for league in city_data.values():
        for team in league.values():
            total += len(team)
    return total

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("Converting all new cities to JSON...\n")
    
    for city in NEW_CITIES:
        print(f"Processing {city}...")
        
        city_data = process_city(city)
        total_venues = get_total_venues(city_data)
        
        # Save to JSON
        output_file = OUTPUT_DIR / f"{city}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(city_data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✓ Saved {output_file} ({total_venues} total venues)")
        print()

if __name__ == '__main__':
    main()
