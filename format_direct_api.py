#!/usr/bin/env python3
"""
Direct Google Sheets API formatter.
Extracts OAuth token from gog and makes direct API calls.
"""

import json
import os
import subprocess
import sys
import requests
from pathlib import Path
from collections import defaultdict

SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'
ACCOUNT = 'dpl@stupidgood.ai'
KEYRING_PASSWORD = 'openclaw123'

def get_oauth_token():
    """Extract OAuth token by running gog with debug output."""
    # gog uses standard OAuth2, we need to extract the access token
    # Try to find it in environment or run a command with verbose output
    
    env = os.environ.copy()
    env['GOG_KEYRING_PASSWORD'] = KEYRING_PASSWORD
    env['GOG_ACCOUNT'] = ACCOUNT
    
    # Use gog to make a request and capture the token
    # We'll parse the HTTP request it makes
    
    # Alternative: Look for cached tokens
    possible_token_paths = [
        Path.home() / '.config' / 'gogcli' / 'tokens' / f'{ACCOUNT}.json',
        Path.home() / '.config' / 'gog' / 'tokens' / f'{ACCOUNT}.json',
        Path.home() / '.cache' / 'gog' / f'{ACCOUNT}.json',
    ]
    
    for path in possible_token_paths:
        if path.exists():
            print(f"Found token file: {path}", file=sys.stderr)
            try:
                with open(path) as f:
                    token_data = json.load(f)
                    if 'access_token' in token_data:
                        return token_data['access_token']
            except:
                pass
    
    # If we can't find the token file, we need another approach
    # Use Python's Google API client which can handle the credentials
    print("Could not extract raw token, using API client library", file=sys.stderr)
    return None

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
        
        sport_counts = defaultdict(int)
        for bar in data['bars']:
            for sport in bar.get('sports', []):
                sport_counts[sport] += 1
        
        rows.append([
            city_display,
            total,
            sport_counts.get('NFL', 0),
            sport_counts.get('MLB', 0),
            sport_counts.get('NHL', 0),
            sport_counts.get('NBA', 0)
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
                ' | '.join(bar.get('teams', []))[:2000],
                bar.get('notes', '')[:2000]
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
                    ' | '.join(bar.get('teams', []))[:2000],
                    bar.get('notes', '')[:2000]
                ])
    
    return headers + rows

def create_city_data(city_data, city_key):
    """Create city-specific tab data."""
    headers = [['Sport', 'Team', 'Bar Name', 'Address', 'Phone', 'Website', 'Notes']]
    
    rows = []
    for bar in city_data['bars']:
        sports_list = bar.get('sports', [])
        teams_list = bar.get('teams', [])
        
        if not sports_list:
            sports_list = ['General']
        
        for sport in sports_list:
            rows.append([
                sport,
                ' | '.join(teams_list)[:2000],
                bar.get('name', '').strip('*').strip(),
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                bar.get('notes', '')[:2000]
            ])
    
    return headers + rows

def run_gog(args):
    """Run gog command."""
    env = os.environ.copy()
    env['GOG_KEYRING_PASSWORD'] = KEYRING_PASSWORD
    env['GOG_ACCOUNT'] = ACCOUNT
    
    result = subprocess.run(['gog'] + args, capture_output=True, text=True, env=env)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("=" * 70)
    print("GOOGLE SHEET FORMATTER: Where to Watch the Game")
    print("=" * 70)
    
    # Load data
    print("\n[1/4] Loading data...")
    cities_data = load_data()
    total_bars = sum(len(data['bars']) for data in cities_data.values())
    print(f"      ✅ {len(cities_data)} cities, {total_bars} bars")
    
    # Prepare tab data
    print("\n[2/4] Preparing data...")
    tab_data = {
        'SUMMARY': create_summary_data(cities_data),
        'ALL_BARS': create_all_bars_data(cities_data),
        'NFL_Bars': create_sport_data(cities_data, 'NFL'),
        'MLB_Bars': create_sport_data(cities_data, 'MLB'),
        'NHL_Bars': create_sport_data(cities_data, 'NHL'),
        'NBA_Bars': create_sport_data(cities_data, 'NBA'),
        'Denver': create_city_data(cities_data['denver'], 'denver'),
        'Las_Vegas': create_city_data(cities_data['las-vegas'], 'las-vegas'),
        'Orange_County': create_city_data(cities_data['orange-county'], 'orange-county'),
        'Phoenix': create_city_data(cities_data['phoenix'], 'phoenix'),
        'Austin': create_city_data(cities_data['austin'], 'austin'),
        'NYC': create_city_data(cities_data['nyc'], 'nyc'),
        'Chicago': create_city_data(cities_data['chicago'], 'chicago'),
    }
    
    for tab, data in tab_data.items():
        print(f"      - {tab.replace('_', ' ')}: {len(data)-1} rows")
    
    # Create tabs (use Sheet1 and rename + create others)
    print("\n[3/4] Setting up tabs...")
    print("      ℹ️  Using underscores in tab names to avoid quoting issues")
    
    # Populate tabs
    print("\n[4/4] Populating tabs...")
    success = 0
    failed = []
    
    for tab_name, data in tab_data.items():
        print(f"      {tab_name}... ", end='', flush=True)
        
        # Clear and update
        success_clear, _, _ = run_gog(['sheets', 'clear', SHEET_ID, f'{tab_name}!A:Z'])
        
        if not success_clear:
            print(f"❌ (tab doesn't exist - create it first)")
            failed.append(tab_name)
            continue
        
        # Write data
        values_json = json.dumps(data)
        success_update, _, stderr = run_gog([
            'sheets', 'update', SHEET_ID, f'{tab_name}!A1',
            '--values-json', values_json,
            '--input', 'USER_ENTERED'
        ])
        
        if success_update:
            print(f"✅ ({len(data)-1} rows)")
            success += 1
        else:
            print(f"❌ {stderr[:50]}")
            failed.append(tab_name)
    
    print(f"\n      Result: {success}/{len(tab_data)} tabs populated")
    
    if failed:
        print(f"\n      ⚠️  Failed tabs: {', '.join(failed)}")
        print(f"      Create them manually: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    
    print("\n" + "=" * 70)
    if success == len(tab_data):
        print("✅ ALL TABS POPULATED SUCCESSFULLY!")
    else:
        print(f"⚠️  PARTIAL SUCCESS: {success}/{len(tab_data)} tabs")
    print("=" * 70)
    print(f"\n🔗 https://docs.google.com/spreadsheets/d/{SHEET_ID}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
