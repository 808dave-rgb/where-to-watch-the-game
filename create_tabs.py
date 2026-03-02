#!/usr/bin/env python3
"""
Create tabs in Google Sheet using direct API access.
Uses subprocess to work around gog's keyring encryption.
"""

import subprocess
import json
import sys

SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'

# Required tabs
TABS = [
    'SUMMARY',
    'ALL BARS',
    'NFL Bars',
    'MLB Bars',
    'NHL Bars',
    'NBA Bars',
    'Denver',
    'Las Vegas',
    'Orange County',
    'Phoenix',
    'Austin',
    'NYC',
    'Chicago'
]

def create_tabs_via_curl():
    """
    Create tabs by making direct API calls using curl with gog's token.
    This is a workaround since gog doesn't support batchUpdate.
    """
    
    # First, get the metadata to see what tabs exist
    result = subprocess.run([
        'bash', '-c',
        f'''
        export GOG_KEYRING_PASSWORD='openclaw123'
        gog sheets metadata {SHEET_ID} --account dpl@stupidgood.ai --json
        '''
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"ERROR: Could not get metadata: {result.stderr}", file=sys.stderr)
        return False
    
    metadata = json.loads(result.stdout)
    existing_tabs = [sheet['properties']['title'] for sheet in metadata['sheets']]
    
    print(f"Existing tabs: {existing_tabs}")
    
    # Determine which tabs to create
    tabs_to_create = [tab for tab in TABS if tab not in existing_tabs]
    
    if not tabs_to_create:
        print("✅ All tabs already exist!")
        return True
    
    print(f"\nNeed to create {len(tabs_to_create)} tabs:")
    for tab in tabs_to_create:
        print(f"  - {tab}")
    
    # We need to use Google Sheets API batchUpdate endpoint
    # But we don't have direct access to the OAuth token from gog
    
    print("\n⚠️  LIMITATION: gog CLI doesn't support creating tabs")
    print("⚠️  Need to create tabs manually or use Google Sheets API directly")
    
    print("\n📝 MANUAL STEPS:")
    print(f"1. Open: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print("2. Create these tabs by clicking '+' at bottom:")
    for tab in tabs_to_create:
        print(f"   - {tab}")
    print("3. Then run the populate script")
    
    return False

if __name__ == '__main__':
    success = create_tabs_via_curl()
    sys.exit(0 if success else 1)
