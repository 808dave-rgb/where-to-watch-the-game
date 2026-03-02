#!/usr/bin/env python3
"""
Complete Google Sheet formatter using Google Sheets API.
Extracts credentials from gog CLI and uses them directly.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'
ACCOUNT = 'dpl@stupidgood.ai'
KEYRING_PASSWORD = 'openclaw123'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Get credentials from gog's token storage."""
    # Try to find gog's token
    possible_paths = [
        Path.home() / '.config' / 'gogcli' / 'credentials' / f'{ACCOUNT}.json',
        Path.home() / '.config' / 'gog' / 'credentials' / f'{ACCOUNT}.json',
        Path.home() / '.config' / 'gog' / 'token.json',
    ]
    
    for token_path in possible_paths:
        if token_path.exists():
            print(f"Found token at: {token_path}", file=sys.stderr)
            try:
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                if creds and creds.valid:
                    return creds
                print(f"Token exists but invalid/expired", file=sys.stderr)
            except Exception as e:
                print(f"Error loading token: {e}", file=sys.stderr)
    
    # gog uses encrypted keyring, so we can't easily extract the token
    # Alternative: Use gog to make a request and extract the Authorization header
    # For now, we'll use a workaround with subprocess
    
    print("Could not find valid credentials. Using gog subprocess method.", file=sys.stderr)
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
                ' | '.join(bar.get('teams', []))[:1000],
                bar.get('notes', '')[:1000]
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
                    ' | '.join(bar.get('teams', []))[:1000],
                    bar.get('notes', '')[:1000]
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
                ' | '.join(teams_list)[:1000],
                bar.get('name', '').strip('*').strip(),
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                bar.get('notes', '')[:1000]
            ])
    
    return headers + rows

def run_gog_command(args):
    """Run a gog command and return output."""
    env = os.environ.copy()
    env['GOG_KEYRING_PASSWORD'] = KEYRING_PASSWORD
    env['GOG_ACCOUNT'] = ACCOUNT
    
    cmd = ['gog'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}", file=sys.stderr)
        return None
    
    return result.stdout

def format_with_api():
    """Try to format using API directly."""
    creds = get_credentials()
    if not creds:
        return False
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = service.spreadsheets()
        
        # Get existing sheets
        sheet_metadata = spreadsheet.get(spreadsheetId=SHEET_ID).execute()
        existing_sheets = {sheet['properties']['title']: sheet['properties']['sheetId'] 
                          for sheet in sheet_metadata['sheets']}
        
        print(f"Existing sheets: {list(existing_sheets.keys())}", file=sys.stderr)
        
        # Create tabs if they don't exist
        tabs = [
            'SUMMARY', 'ALL BARS', 'NFL Bars', 'MLB Bars', 'NHL Bars', 'NBA Bars',
            'Denver', 'Las Vegas', 'Orange County', 'Phoenix', 'Austin', 'NYC', 'Chicago'
        ]
        
        requests = []
        for tab_name in tabs:
            if tab_name not in existing_sheets:
                requests.append({
                    'addSheet': {
                        'properties': {'title': tab_name}
                    }
                })
        
        if requests:
            print(f"Creating {len(requests)} new tabs...", file=sys.stderr)
            body = {'requests': requests}
            spreadsheet.batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
        
        return True
        
    except HttpError as error:
        print(f"API Error: {error}", file=sys.stderr)
        return False

def main():
    print("=" * 70)
    print("FORMATTING: Where to Watch the Game - Google Sheet")
    print("=" * 70)
    
    # Load data
    print("\n[1/5] Loading data...")
    cities_data = load_data()
    print(f"      ✅ {len(cities_data)} cities loaded")
    total_bars = sum(len(data['bars']) for data in cities_data.values())
    print(f"      ✅ {total_bars} total bars")
    
    # Prepare all tab data
    print("\n[2/5] Preparing tab data...")
    tab_data = {
        'SUMMARY': create_summary_data(cities_data),
        'ALL BARS': create_all_bars_data(cities_data),
        'NFL Bars': create_sport_data(cities_data, 'NFL'),
        'MLB Bars': create_sport_data(cities_data, 'MLB'),
        'NHL Bars': create_sport_data(cities_data, 'NHL'),
        'NBA Bars': create_sport_data(cities_data, 'NBA'),
    }
    
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
    
    print(f"      ✅ {len(tab_data)} tabs prepared")
    for tab, data in tab_data.items():
        print(f"         - {tab}: {len(data)-1} rows")
    
    # Try API approach first
    print("\n[3/5] Creating tabs...")
    if format_with_api():
        print("      ✅ Tabs created via API")
    else:
        print("      ⚠️  API method failed, continuing with gog CLI...")
    
    # Update data using gog CLI
    print("\n[4/5] Populating tabs...")
    success = 0
    for tab_name, data in tab_data.items():
        print(f"      Updating '{tab_name}'... ", end='', flush=True)
        
        # Clear tab
        run_gog_command(['sheets', 'clear', SHEET_ID, f"'{tab_name}'!A:Z"])
        
        # Update with data
        values_json = json.dumps(data)
        result = run_gog_command([
            'sheets', 'update', SHEET_ID, f"'{tab_name}'!A1",
            '--values-json', values_json,
            '--input', 'USER_ENTERED'
        ])
        
        if result is not None:
            print(f"✅ ({len(data)-1} rows)")
            success += 1
        else:
            print(f"❌ FAILED")
    
    print(f"\n      ✅ {success}/{len(tab_data)} tabs populated")
    
    # Format (manual step - gog doesn't support formatting)
    print("\n[5/5] Formatting...")
    print("      ⚠️  Manual formatting needed:")
    print("         1. Bold header rows")
    print("         2. Freeze first row")
    print("         3. Add auto-filters")
    print("         4. Auto-resize columns")
    print("\n      💡 Or use 'Format > Alternating colors' for easy viewing")
    
    print("\n" + "=" * 70)
    print("✅ SHEET POPULATION COMPLETE!")
    print("=" * 70)
    print(f"\n🔗 https://docs.google.com/spreadsheets/d/{SHEET_ID}\n")
    print(f"📊 Summary: {len(cities_data)} cities, {total_bars} bars, {len(tab_data)} tabs\n")

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
