# Google Sheet Setup Instructions

## Current Status

✅ Summary data populated in Sheet1

## Next Steps

### 1. Open the Google Sheet

🔗 https://docs.google.com/spreadsheets/d/1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o/edit

### 2. Rename Sheet1

- Right-click on "Sheet1" tab at the bottom
- Select "Rename"
- Change to: **SUMMARY**

### 3. Create 12 Additional Tabs

Click the "+" button at the bottom left to add each of these tabs:

**All Bars Tab:**
1. `ALL_BARS`

**Sport Tabs (4):**
2. `NFL_Bars`
3. `MLB_Bars`
4. `NHL_Bars`
5. `NBA_Bars`

**City Tabs (7):**
6. `Denver`
7. `Las_Vegas`
8. `Orange_County`
9. `Phoenix`
10. `Austin`
11. `NYC`
12. `Chicago`

💡 **Note:** Use underscores (_) not spaces in tab names to avoid command-line quoting issues

### 4. Run the Population Script

Once all tabs are created, run:

```bash
cd /data/.openclaw/workspace/where-to-watch-the-game
python3 format_direct_api.py
```

This will:
- Load data from all 7 city JSON files (640 total bars)
- Populate each tab with properly formatted data
- Add headers to each tab

### 5. Final Formatting (Optional)

After population, you can manually:
- **Bold the header rows** (row 1 in each tab)
- **Freeze the top row** (View → Freeze → 1 row)
- **Add filters** (Data → Create a filter)
- **Auto-resize columns** (Select all → Format → Column width → Fit to data)
- **Add alternating colors** (Format → Alternating colors)

## Tab Structure

### SUMMARY Tab
- Columns: City, Total Bars, NFL Bars, MLB Bars, NHL Bars, NBA Bars
- 7 data rows (one per city)

### ALL_BARS Tab
- Columns: City, Bar Name, Address, Phone, Website, Sports, Teams, Notes
- 640 data rows (all bars from all cities)

### Sport Tabs (NFL_Bars, MLB_Bars, NHL_Bars, NBA_Bars)
- Columns: City, Bar Name, Address, Phone, Website, Teams, Notes
- Filtered by sport

### City Tabs (Denver, Las_Vegas, etc.)
- Columns: Sport, Team, Bar Name, Address, Phone, Website, Notes
- All bars for that specific city

## Troubleshooting

**If a tab fails to populate:**
1. Check that the tab name matches exactly (including underscores)
2. Make sure the tab exists before running the script
3. Check the error message - it will tell you which tab failed

**If you want different tab names:**
1. Edit `format_direct_api.py`
2. Find the `tab_data` dictionary
3. Change the keys to your preferred names
4. Create tabs with those exact names

## Data Sources

Data compiled from:
- JSON files in `data/` directory
- 7 cities: Austin, Chicago, Denver, Las Vegas, NYC, Orange County, Phoenix
- 4 sports: NFL, MLB, NHL, NBA
- Last updated: March 1, 2026
