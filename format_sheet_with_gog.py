#!/usr/bin/env python3
"""
Format Google Sheet using gog CLI and direct API calls.
This script uses the GOG_KEYRING_PASSWORD to access gog's credentials.
"""

import json
import os
import subprocess
from pathlib import Path
from collections import defaultdict
import sys

SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'
ACCOUNT = 'dpl@stupidgood.ai'
KEYRING_PASSWORD = 'openclaw123'

def run_gog(args):
    """Run gog command with credentials."""
    env = os.environ.copy()
    env['GOG_KEYRING_PASSWORD'] = KEYRING_PASSWORD
    env['GOG_ACCOUNT'] = ACCOUNT
    
    cmd = ['gog'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    if result.returncode != 0:
        print(f"ERROR running: {' '.join(cmd)}", file=sys.stderr)
        print(f"STDERR: {result.stderr}", file=sys.stderr)
        return None
    
    return result.stdout

def load_data():
    """Load all city JSON files."""
    data_dir = Path(__file__).parent / 'data'
    cities_data = {}
    
    for json_file in sorted(data_dir.glob('*.json')):
        city_name = json_file.stem
        with open(json_file) as f:
            cities_data[city_name] = json.load(f)
    
    return cities_data

def create_summary_data(cities_data):
    """Create summary tab data."""
    headers = [['City', 'Total Bars', 'NFL Bars', 'MLB Bars', 'NHL Bars', 'NBA Bars']]
    
    city_name_map = {
        'austin': 'Austin',
        'chicago': 'Chicago',
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'nyc': 'NYC',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix'
    }
    
    rows = []
    for city_key, data in sorted(cities_data.items()):
        city_display = city_name_map.get(city_key, city_key.title())
        total = data.get('total_bars', len(data['bars']))
        
        # Count by sport
        sport_counts = defaultdict(int)
        for bar in data['bars']:
            for sport in bar.get('sports', []):
                sport_counts[sport] += 1
        
        rows.append([
            city_display,
            str(total),
            str(sport_counts.get('NFL', 0)),
            str(sport_counts.get('MLB', 0)),
            str(sport_counts.get('NHL', 0)),
            str(sport_counts.get('NBA', 0))
        ])
    
    return headers + rows

def create_all_bars_data(cities_data):
    """Create all bars tab data."""
    headers = [['City', 'Bar Name', 'Address', 'Phone', 'Website', 'Sports', 'Teams', 'Notes']]
    
    city_name_map = {
        'austin': 'Austin',
        'chicago': 'Chicago',
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'nyc': 'NYC',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix'
    }
    
    rows = []
    for city_key, data in sorted(cities_data.items()):
        city_display = city_name_map.get(city_key, city_key.title())
        for bar in data['bars']:
            rows.append([
                city_display,
                bar.get('name', '').strip('*').strip(),
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                ', '.join(bar.get('sports', [])),
                ' | '.join(bar.get('teams', []))[:500],  # Limit length
                bar.get('notes', '')[:500]  # Limit length
            ])
    
    return headers + rows

def create_sport_data(cities_data, sport):
    """Create sport-specific tab data."""
    headers = [['City', 'Bar Name', 'Address', 'Phone', 'Website', 'Teams', 'Notes']]
    
    city_name_map = {
        'austin': 'Austin',
        'chicago': 'Chicago',
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'nyc': 'NYC',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix'
    }
    
    rows = []
    for city_key, data in sorted(cities_data.items()):
        city_display = city_name_map.get(city_key, city_key.title())
        for bar in data['bars']:
            if sport in bar.get('sports', []):
                rows.append([
                    city_display,
                    bar.get('name', '').strip('*').strip(),
                    bar.get('address', ''),
                    bar.get('phone', ''),
                    bar.get('website', ''),
                    ' | '.join(bar.get('teams', []))[:500],
                    bar.get('notes', '')[:500]
                ])
    
    return headers + rows

def create_city_data(city_data, city_key):
    """Create city-specific tab data."""
    headers = [['Sport', 'Team', 'Bar Name', 'Address', 'Phone', 'Website', 'Notes']]
    
    rows = []
    for bar in city_data['bars']:
        sports_list = bar.get('sports', [])
        teams_list = bar.get('teams', [])
        
        # Create one row per sport
        if not sports_list:
            sports_list = ['General']
        
        for sport in sports_list:
            rows.append([
                sport,
                ' | '.join(teams_list)[:500],
                bar.get('name', '').strip('*').strip(),
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                bar.get('notes', '')[:500]
            ])
    
    return headers + rows

def clear_and_update_sheet(tab_name, data):
    """Clear a sheet range and update with new data."""
    print(f"  Updating {tab_name}... ({len(data)-1} rows)")
    
    # Clear existing data
    run_gog(['sheets', 'clear', SHEET_ID, f"'{tab_name}'!A:Z", '--account', ACCOUNT])
    
    # Update with new data
    values_json = json.dumps(data)
    result = run_gog(['sheets', 'update', SHEET_ID, f"'{tab_name}'!A1", 
                     '--values-json', values_json, '--input', 'USER_ENTERED', '--account', ACCOUNT])
    
    return result is not None

def main():
    print("=" * 60)
    print("FORMATTING GOOGLE SHEET: Where to Watch the Game")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    cities_data = load_data()
    print(f"   ✅ Loaded {len(cities_data)} cities")
    
    total_bars = sum(len(data['bars']) for data in cities_data.values())
    print(f"   ✅ Total bars: {total_bars}")
    
    # Get current sheet info
    print("\n2. Checking current sheet...")
    metadata = run_gog(['sheets', 'metadata', SHEET_ID, '--json', '--account', ACCOUNT])
    if metadata:
        meta = json.loads(metadata)
        print(f"   ✅ Sheet: {meta['title']}")
        print(f"   ✅ Existing tabs: {[s['properties']['title'] for s in meta['sheets']]}")
    
    # Note: gog CLI doesn't support adding tabs via batchUpdate
    # We'll need to use existing tabs or create them manually
    print("\n3. Preparing data for tabs...")
    
    tab_data = {
        'SUMMARY': create_summary_data(cities_data),
        'ALL BARS': create_all_bars_data(cities_data),
        'NFL Bars': create_sport_data(cities_data, 'NFL'),
        'MLB Bars': create_sport_data(cities_data, 'MLB'),
        'NHL Bars': create_sport_data(cities_data, 'NHL'),
        'NBA Bars': create_sport_data(cities_data, 'NBA'),
    }
    
    # Add city tabs
    city_name_map = {
        'austin': 'Austin',
        'chicago': 'Chicago',
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'nyc': 'NYC',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix'
    }
    
    for city_key, city_display in city_name_map.items():
        tab_data[city_display] = create_city_data(cities_data[city_key], city_key)
    
    print(f"   ✅ Prepared {len(tab_data)} tabs")
    
    print("\n4. Updating sheet tabs...")
    print("   ⚠️  NOTE: Tabs must exist! Create them manually first if needed.")
    print("   ⚠️  Go to sheet and add tabs: SUMMARY, ALL BARS, NFL Bars, MLB Bars, NHL Bars, NBA Bars,")
    print("   ⚠️  Denver, Las Vegas, Orange County, Phoenix, Austin, NYC, Chicago")
    
    input("\n   Press ENTER when tabs are created (or Ctrl+C to cancel)...")
    
    print("\n5. Populating tabs...")
    success_count = 0
    for tab_name, data in tab_data.items():
        if clear_and_update_sheet(tab_name, data):
            success_count += 1
    
    print(f"\n   ✅ Updated {success_count}/{len(tab_data)} tabs")
    
    print("\n6. Formatting notes:")
    print("   ⚠️  Bold headers, freeze rows, and filters must be applied manually")
    print("   ⚠️  Or use Google Sheets API directly (requires more auth setup)")
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE!")
    print("=" * 60)
    print(f"\n🔗 View sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
