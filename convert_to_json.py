#!/usr/bin/env python3
"""
Convert markdown research files to unified JSON format for web app
"""
import json
import re
from pathlib import Path

def parse_markdown_bars(file_path):
    """Parse markdown file with bar listings"""
    bars = []
    current_team = None
    current_bar = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.rstrip()
        
        # Team header (## Team Name)
        if line.startswith('## ') and not line.startswith('###'):
            current_team = line[3:].strip()
            continue
        
        # Bar name (### Bar Name)
        if line.startswith('### '):
            # Save previous bar if exists
            if current_bar and current_bar.get('name'):
                bars.append(current_bar)
            
            # Start new bar
            current_bar = {
                'name': line[4:].strip(),
                'teams': [current_team] if current_team else [],
                'address': '',
                'phone': '',
                'website': '',
                'notes': ''
            }
            continue
        
        # Parse bar details
        if current_bar:
            if line.startswith('- Address:'):
                current_bar['address'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Phone:'):
                current_bar['phone'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Website:'):
                current_bar['website'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Notes:'):
                current_bar['notes'] = line.split(':', 1)[1].strip()
            elif line.startswith('- Source:'):
                if 'notes' in current_bar and current_bar['notes']:
                    current_bar['notes'] += ' | ' + line.split(':', 1)[1].strip()
                else:
                    current_bar['notes'] = line.split(':', 1)[1].strip()
    
    # Save last bar
    if current_bar and current_bar.get('name'):
        bars.append(current_bar)
    
    return bars

def extract_sport_from_filename(filename):
    """Extract sport from filename like 'vegas-nfl-bars.md'"""
    parts = filename.lower().replace('.md', '').split('-')
    for part in ['nfl', 'nba', 'mlb', 'nhl']:
        if part in parts:
            return part.upper()
    return 'UNKNOWN'

def extract_city_from_filename(filename):
    """Extract city from filename"""
    filename = filename.lower().replace('.md', '')
    if 'vegas' in filename:
        return 'las-vegas'
    elif 'oc' in filename:
        return 'orange-county'
    elif 'denver' in filename:
        return 'denver'
    return 'unknown'

def consolidate_bars(bars):
    """Consolidate duplicate bars (same name) and merge their teams"""
    bar_dict = {}
    
    for bar in bars:
        name = bar['name'].strip()
        if name in bar_dict:
            # Merge teams
            existing_teams = set(bar_dict[name]['teams'])
            new_teams = set(bar['teams'])
            bar_dict[name]['teams'] = sorted(list(existing_teams | new_teams))
            
            # Update fields if they were empty
            for field in ['address', 'phone', 'website', 'notes']:
                if not bar_dict[name].get(field) and bar.get(field):
                    bar_dict[name][field] = bar[field]
        else:
            bar_dict[name] = bar
    
    return list(bar_dict.values())

def geocode_address(address):
    """Placeholder for geocoding - returns None for now"""
    # TODO: Add geocoding logic or use existing geocoded data
    return None

def main():
    research_dir = Path('/data/.openclaw/workspace/research')
    output_dir = Path('/data/.openclaw/workspace/where-to-watch-the-game/data')
    output_dir.mkdir(exist_ok=True)
    
    # Process files by city
    cities = {
        'denver': [],
        'las-vegas': [],
        'orange-county': []
    }
    
    # Find all bar markdown files
    for md_file in research_dir.glob('*.md'):
        filename = md_file.name
        
        # Skip non-bar files
        if not any(sport in filename.lower() for sport in ['nfl', 'nba', 'mlb', 'nhl']):
            continue
        
        city = extract_city_from_filename(filename)
        sport = extract_sport_from_filename(filename)
        
        if city not in cities:
            continue
        
        print(f"Processing {filename} -> {city} / {sport}")
        
        bars = parse_markdown_bars(md_file)
        
        # Add sport and city metadata
        for bar in bars:
            if 'sports' not in bar:
                bar['sports'] = []
            if sport not in bar['sports']:
                bar['sports'].append(sport)
            bar['city'] = city
        
        cities[city].extend(bars)
    
    # Consolidate and save each city
    for city, bars in cities.items():
        if not bars:
            print(f"⚠️  No bars found for {city}")
            continue
        
        # Consolidate duplicates
        consolidated = consolidate_bars(bars)
        
        # Sort by name
        consolidated.sort(key=lambda x: x['name'])
        
        # Group by sport
        by_sport = {}
        for bar in consolidated:
            for sport in bar.get('sports', []):
                if sport not in by_sport:
                    by_sport[sport] = []
                by_sport[sport].append(bar)
        
        # Save city data
        city_data = {
            'city': city,
            'total_bars': len(consolidated),
            'sports': list(by_sport.keys()),
            'bars': consolidated,
            'by_sport': by_sport
        }
        
        output_file = output_dir / f'{city}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(city_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {city}: {len(consolidated)} bars saved to {output_file}")
        for sport, sport_bars in by_sport.items():
            print(f"   - {sport}: {len(sport_bars)} bars")

if __name__ == '__main__':
    main()
