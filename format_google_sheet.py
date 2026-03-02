#!/usr/bin/env python3
"""
Format Google Sheet with "Where to Watch the Game" data.
Creates 13 tabs: Summary, All Bars, 4 sport tabs, 7 city tabs.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Google Sheets API setup
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'

def load_data():
    """Load all city JSON files."""
    data_dir = Path(__file__).parent / 'data'
    cities_data = {}
    
    for json_file in data_dir.glob('*.json'):
        city_name = json_file.stem
        with open(json_file) as f:
            cities_data[city_name] = json.load(f)
    
    return cities_data

def create_summary_tab(cities_data):
    """Create summary tab data."""
    headers = ['City', 'Total Bars', 'NFL Bars', 'MLB Bars', 'NHL Bars', 'NBA Bars']
    rows = [headers]
    
    city_name_map = {
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix',
        'austin': 'Austin',
        'nyc': 'NYC',
        'chicago': 'Chicago'
    }
    
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
            total,
            sport_counts.get('NFL', 0),
            sport_counts.get('MLB', 0),
            sport_counts.get('NHL', 0),
            sport_counts.get('NBA', 0)
        ])
    
    return rows

def create_all_bars_tab(cities_data):
    """Create all bars tab data."""
    headers = ['City', 'Bar Name', 'Address', 'Phone', 'Website', 'Sports', 'Teams', 'Notes']
    rows = [headers]
    
    city_name_map = {
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix',
        'austin': 'Austin',
        'nyc': 'NYC',
        'chicago': 'Chicago'
    }
    
    for city_key, data in sorted(cities_data.items()):
        city_display = city_name_map.get(city_key, city_key.title())
        for bar in data['bars']:
            rows.append([
                city_display,
                bar.get('name', '').strip('*'),  # Remove markdown bold
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                ', '.join(bar.get('sports', [])),
                ', '.join(bar.get('teams', [])),
                bar.get('notes', '')
            ])
    
    return rows

def create_sport_tab(cities_data, sport):
    """Create sport-specific tab data."""
    headers = ['City', 'Bar Name', 'Address', 'Phone', 'Website', 'Teams', 'Notes']
    rows = [headers]
    
    city_name_map = {
        'denver': 'Denver',
        'las-vegas': 'Las Vegas',
        'orange-county': 'Orange County',
        'phoenix': 'Phoenix',
        'austin': 'Austin',
        'nyc': 'NYC',
        'chicago': 'Chicago'
    }
    
    for city_key, data in sorted(cities_data.items()):
        city_display = city_name_map.get(city_key, city_key.title())
        for bar in data['bars']:
            if sport in bar.get('sports', []):
                rows.append([
                    city_display,
                    bar.get('name', '').strip('*'),
                    bar.get('address', ''),
                    bar.get('phone', ''),
                    bar.get('website', ''),
                    ', '.join(bar.get('teams', [])),
                    bar.get('notes', '')
                ])
    
    return rows

def create_city_tab(city_data, city_key):
    """Create city-specific tab data."""
    headers = ['Sport', 'Team', 'Bar Name', 'Address', 'Phone', 'Website', 'Notes']
    rows = [headers]
    
    for bar in city_data['bars']:
        sports_list = bar.get('sports', [])
        teams_list = bar.get('teams', [])
        
        # Create one row per sport
        for sport in sports_list:
            rows.append([
                sport,
                ', '.join(teams_list),
                bar.get('name', '').strip('*'),
                bar.get('address', ''),
                bar.get('phone', ''),
                bar.get('website', ''),
                bar.get('notes', '')
            ])
    
    return rows

def format_sheet():
    """Main function to format the Google Sheet."""
    print("Loading data...")
    cities_data = load_data()
    print(f"Loaded {len(cities_data)} cities")
    
    # Load credentials
    creds = None
    token_path = Path.home() / '.config' / 'gog' / 'token.json'
    
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    else:
        print("ERROR: No gog credentials found. Run 'gog auth add' first.")
        return
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = service.spreadsheets()
        
        print("\nCreating tabs...")
        
        # Get existing sheets
        sheet_metadata = spreadsheet.get(spreadsheetId=SHEET_ID).execute()
        existing_sheets = {sheet['properties']['title']: sheet['properties']['sheetId'] 
                          for sheet in sheet_metadata['sheets']}
        
        # Define tabs to create
        tabs = [
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
        
        # Clear/create tabs
        requests = []
        
        for tab_name in tabs:
            if tab_name not in existing_sheets:
                # Create new tab
                requests.append({
                    'addSheet': {
                        'properties': {
                            'title': tab_name
                        }
                    }
                })
        
        if requests:
            body = {'requests': requests}
            spreadsheet.batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
            print(f"Created {len(requests)} new tabs")
        
        # Populate tabs
        print("\nPopulating tabs...")
        
        # 1. Summary tab
        print("  - SUMMARY")
        summary_data = create_summary_tab(cities_data)
        spreadsheet.values().update(
            spreadsheetId=SHEET_ID,
            range='SUMMARY!A1',
            valueInputOption='USER_ENTERED',
            body={'values': summary_data}
        ).execute()
        
        # 2. All Bars tab
        print("  - ALL BARS")
        all_bars_data = create_all_bars_tab(cities_data)
        spreadsheet.values().update(
            spreadsheetId=SHEET_ID,
            range='ALL BARS!A1',
            valueInputOption='USER_ENTERED',
            body={'values': all_bars_data}
        ).execute()
        
        # 3-6. Sport tabs
        for sport in ['NFL', 'MLB', 'NHL', 'NBA']:
            print(f"  - {sport} Bars")
            sport_data = create_sport_tab(cities_data, sport)
            spreadsheet.values().update(
                spreadsheetId=SHEET_ID,
                range=f'{sport} Bars!A1',
                valueInputOption='USER_ENTERED',
                body={'values': sport_data}
            ).execute()
        
        # 7-13. City tabs
        city_name_map = {
            'denver': 'Denver',
            'las-vegas': 'Las Vegas',
            'orange-county': 'Orange County',
            'phoenix': 'Phoenix',
            'austin': 'Austin',
            'nyc': 'NYC',
            'chicago': 'Chicago'
        }
        
        for city_key, city_display in city_name_map.items():
            print(f"  - {city_display}")
            city_data = create_city_tab(cities_data[city_key], city_key)
            spreadsheet.values().update(
                spreadsheetId=SHEET_ID,
                range=f'{city_display}!A1',
                valueInputOption='USER_ENTERED',
                body={'values': city_data}
            ).execute()
        
        # Format all tabs
        print("\nFormatting tabs...")
        
        # Refresh sheet metadata
        sheet_metadata = spreadsheet.get(spreadsheetId=SHEET_ID).execute()
        sheet_ids = {sheet['properties']['title']: sheet['properties']['sheetId'] 
                    for sheet in sheet_metadata['sheets']}
        
        format_requests = []
        
        for tab_name in tabs:
            if tab_name not in sheet_ids:
                continue
                
            sheet_id = sheet_ids[tab_name]
            
            # Bold header row
            format_requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {
                                'bold': True
                            }
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat.bold'
                }
            })
            
            # Freeze header row
            format_requests.append({
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': sheet_id,
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            })
            
            # Auto-resize columns
            format_requests.append({
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 10
                    }
                }
            })
            
            # Add filter
            format_requests.append({
                'setBasicFilter': {
                    'filter': {
                        'range': {
                            'sheetId': sheet_id
                        }
                    }
                }
            })
        
        if format_requests:
            body = {'requests': format_requests}
            spreadsheet.batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()
            print(f"Applied formatting to {len(tabs)} tabs")
        
        print("\n✅ Sheet formatting complete!")
        print(f"🔗 https://docs.google.com/spreadsheets/d/{SHEET_ID}")
        
    except HttpError as error:
        print(f"ERROR: {error}")
        raise

if __name__ == '__main__':
    format_sheet()
