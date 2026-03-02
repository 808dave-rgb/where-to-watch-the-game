# 🎯 Finish Google Sheet Setup - 2 Steps

## Current Status

✅ Summary data is already populated in the sheet!

View it here: https://docs.google.com/spreadsheets/d/1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o/edit

## What You Need to Do (5 minutes)

### Step 1: Create Tabs (3 minutes)

Open the sheet and create these 13 tabs by clicking the "+" button at the bottom:

**Required Tab Names (copy/paste these exactly):**

```
SUMMARY
ALL_BARS
NFL_Bars
MLB_Bars
NHL_Bars
NBA_Bars
Denver
Las_Vegas
Orange_County
Phoenix
Austin
NYC
Chicago
```

**Tips:**
- You can rename "Sheet1" to "SUMMARY" (right-click → Rename)
- Use underscores, not spaces
- Names are case-sensitive

### Step 2: Run the Script (2 minutes)

```bash
cd /data/.openclaw/workspace/where-to-watch-the-game
python3 format_direct_api.py
```

This will populate all 640 bars across all tabs.

## What You'll Get

✅ **13 Organized Tabs:**
- 1 Summary tab (city statistics)
- 1 Complete database (all 640 bars)
- 4 Sport-specific tabs (NFL, MLB, NHL, NBA)
- 7 City-specific tabs (one per city)

✅ **Clean Data:**
- Headers on every tab
- Organized by City, Bar Name, Address, Phone, Website, etc.
- Ready to filter and search

## Optional: Pretty Formatting (2 minutes)

After the script runs, you can make it look nicer:

1. **Bold headers**: Select row 1 → Click "B" (bold)
2. **Freeze top row**: View → Freeze → 1 row
3. **Add filters**: Data → Create a filter
4. **Auto-resize**: Select all → Format → Column width → Fit to data
5. **Alternating colors**: Format → Alternating colors → Choose a theme

## Why Manual Tab Creation?

The `gog` CLI tool we're using doesn't support creating tabs programmatically. The alternative (Google Sheets API with service account) would take 30+ minutes to set up. This way is faster!

## Need Help?

See `SETUP_INSTRUCTIONS.md` for detailed instructions.

---

**Ready?** Open the sheet and create those 13 tabs! 🚀
