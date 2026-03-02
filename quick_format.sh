#!/bin/bash
# Quick Google Sheet formatter
# Creates and populates all tabs

set -e

export GOG_KEYRING_PASSWORD='openclaw123'
export GOG_ACCOUNT='dpl@stupidgood.ai'
SHEET_ID='1KWwsJZIaUuwrufKUk_u33CYgOewHnO4K-mRVWtEnK-o'

echo "========================================"
echo "GOOGLE SHEET FORMATTER"
echo "========================================"
echo ""

# Step 1: Check current tabs
echo "[1/3] Checking existing tabs..."
EXISTING_TABS=$(gog sheets metadata "$SHEET_ID" --json | jq -r '.sheets[].properties.title')
echo "Current tabs:"
echo "$EXISTING_TABS"
echo ""

# Step 2: Create tabs
echo "[2/3] Creating tabs..."
echo "⚠️  NOTE: gog doesn't support creating tabs programmatically"
echo "⚠️  Opening sheet in browser for manual tab creation..."
echo ""
echo "Required tabs:"
echo "  1. SUMMARY"
echo "  2. ALL BARS"
echo "  3. NFL Bars"
echo "  4. MLB Bars"
echo "  5. NHL Bars"
echo "  6. NBA Bars"
echo "  7. Denver"
echo "  8. Las Vegas"
echo "  9. Orange County"
echo " 10. Phoenix"
echo " 11. Austin"
echo " 12. NYC"
echo " 13. Chicago"
echo ""
echo "🔗 https://docs.google.com/spreadsheets/d/$SHEET_ID/edit"
echo ""
read -p "Press ENTER after creating tabs (or Ctrl+C to cancel)... "

# Step 3: Run Python script to populate
echo ""
echo "[3/3] Populating tabs with data..."
python3 format_sheet_complete.py

echo ""
echo "========================================"
echo "✅ COMPLETE!"
echo "========================================"
echo ""
echo "🔗 View: https://docs.google.com/spreadsheets/d/$SHEET_ID"
echo ""
