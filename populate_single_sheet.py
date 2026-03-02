#!/usr/bin/env python3
"""
Populate Sheet1 with formatted data.
User can then manually create tabs and move sections.

OR: Create properly named tabs first, then run format_direct_api.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'
ACCOUNT = 'dpl@stupidgood.ai'
KEYRING_PASSWORD = 'openclaw123'

def run_gog(args):
    """Run gog command."""
    env = os.environ.copy()
    env['GOG_KEYRING_PASSWORD'] = KEYRING_PASSWORD
    env['GOG_ACCOUNT'] = ACCOUNT
    
    result = subprocess.run(['gog'] + args, capture_output=True, text=True, env=env)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    print("=" * 70)
    print("TAB SETUP GUIDE")
    print("=" * 70)
    print("\nThis script will help you set up the Google Sheet properly.")
    print("\nOPTION 1: Manual tab creation (recommended)")
    print("-" * 70)
    print("1. Open the sheet in your browser:")
    print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    print("\n2. Rename 'Sheet1' to 'SUMMARY'")
    print("\n3. Create 12 additional tabs by clicking '+' at the bottom:")
    print("   - ALL_BARS")
    print("   - NFL_Bars")
    print("   - MLB_Bars")
    print("   - NHL_Bars")
    print("   - NBA_Bars")
    print("   - Denver")
    print("   - Las_Vegas")
    print("   - Orange_County")
    print("   - Phoenix")
    print("   - Austin")
    print("   - NYC")
    print("   - Chicago")
    print("\n4. Run: python3 format_direct_api.py")
    print("\n" + "=" * 70)
    print("\nOPTION 2: Use Google Sheets API (advanced)")
    print("-" * 70)
    print("Set up service account credentials and modify the script to create")
    print("tabs programmatically using batchUpdate API.")
    print("\n" + "=" * 70)
    
    print("\nWhich would you like to do?")
    print("  1) I'll create the tabs manually (press 1)")
    print("  2) Show me the data summary (press 2)")
    print("  3) Exit (press 3)")
    
    choice = input("\nChoice: ").strip()
    
    if choice == '2':
        # Load and show data summary
        from format_direct_api import load_data, create_summary_data
        
        print("\n" + "=" * 70)
        print("DATA SUMMARY")
        print("=" * 70)
        
        cities_data = load_data()
        total_bars = sum(len(data['bars']) for data in cities_data.values())
        
        print(f"\nTotal: {len(cities_data)} cities, {total_bars} bars\n")
        
        summary = create_summary_data(cities_data)
        for row in summary:
            if row == summary[0]:
                # Header
                print(" | ".join(f"{cell:15}" for cell in row))
                print("-" * 70)
            else:
                print(" | ".join(f"{str(cell):15}" for cell in row))
        
        print("\n" + "=" * 70)
    elif choice == '1':
        print("\n✅ Great! Follow the steps above, then run:")
        print("   python3 format_direct_api.py")
    else:
        print("\n👋 Exiting")
    
    print("")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
