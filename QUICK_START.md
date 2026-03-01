# ⚡ Quick Start Guide

Get your site live in 5 minutes!

## 🎯 What You Have

A complete, ready-to-deploy sports bar directory website with:
- ✅ 279+ bars across 3 cities (Denver, Vegas, Orange County)
- ✅ Interactive landing page with map
- ✅ Searchable city directory pages
- ✅ All data converted to JSON
- ✅ Mobile-responsive design
- ✅ Zero dependencies (vanilla JS)

## 📂 Location

```
/data/.openclaw/workspace/where-to-watch-the-game/
```

## 🚀 Deploy to GitHub (5 steps)

### 1. Create GitHub Repo

Go to: https://github.com/new
- Name: `where-to-watch-the-game`
- Public repository
- Don't initialize with README
- Click Create

### 2. Connect & Push

```bash
cd /data/.openclaw/workspace/where-to-watch-the-game

# Connect to GitHub
git remote add origin https://github.com/808dave-rgb/where-to-watch-the-game.git

# Push
git push -u origin main
```

### 3. Enable Pages

- Go to repo Settings → Pages
- Source: `main` branch, `/ (root)` folder
- Save

### 4. Wait 2 minutes

Your site builds automatically

### 5. Visit Your Site

```
https://808dave-rgb.github.io/where-to-watch-the-game
```

## 🎉 Done!

You now have a live sports bar directory website.

## 📱 Test Locally First

```bash
cd /data/.openclaw/workspace/where-to-watch-the-game
python3 -m http.server 8000
```

Visit: http://localhost:8000

## 🔄 Update Later

```bash
# Make changes, then:
./deploy.sh

# Or manually:
git add .
git commit -m "Updated data"
git push
```

## 📖 Full Details

- Complete deployment: See `DEPLOYMENT_GUIDE.md`
- Project info: See `README.md`
- Data format: See `README.md` → Data Format section

## 🛠️ Files Explained

| File | Purpose |
|------|---------|
| `index.html` | Landing page with map |
| `cities/*.html` | City directory pages |
| `data/*.json` | Bar data for each city |
| `convert_to_json.py` | Convert markdown to JSON |
| `generate_city_pages.py` | Generate city HTML pages |
| `deploy.sh` | Easy deployment script |

## 🎯 Tech Stack

- Pure HTML/CSS/JavaScript (no build step)
- Leaflet.js for maps (loaded from CDN)
- GitHub Pages for free hosting

## 📊 Current Data

- **Denver:** 138 bars (77 NFL, 29 NBA, 27 NHL, 5 MLB)
- **Las Vegas:** 61 bars (40 NFL, 9 NHL, 6 MLB, 6 NBA)
- **Orange County:** 80 bars (39 MLB, 30 NFL, 6 NBA, 5 NHL)

## ⚠️ Need Help?

- Authentication issues? See `DEPLOYMENT_GUIDE.md` → Step 3
- Site not loading? Check Settings → Pages
- Changes not showing? Hard refresh (Ctrl+Shift+R)

---

**Ready to launch? Let's do this! 🚀**
