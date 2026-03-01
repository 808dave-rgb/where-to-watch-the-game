# ✅ Deployment Checklist

Use this as your step-by-step guide to get your site live.

## Pre-Deployment

- [x] ✅ Data converted from markdown to JSON (279 bars)
- [x] ✅ Landing page created with interactive map
- [x] ✅ City pages generated (Denver, Vegas, OC)
- [x] ✅ All documentation written
- [x] ✅ Git repository initialized
- [x] ✅ Initial commit created

## Deployment Steps

### Step 1: Create GitHub Repository
- [ ] Go to https://github.com/new
- [ ] Name: `where-to-watch-the-game`
- [ ] Visibility: **Public** (required for free Pages)
- [ ] **Don't** initialize with README
- [ ] Click **Create repository**

### Step 2: Connect Local to GitHub
```bash
cd /data/.openclaw/workspace/where-to-watch-the-game
git remote add origin https://github.com/808dave-rgb/where-to-watch-the-game.git
```

- [ ] Remote added successfully

### Step 3: Push to GitHub
```bash
git push -u origin main
```

**If authentication fails:**
- [ ] Option A: Create Personal Access Token at https://github.com/settings/tokens/new
  - Scopes needed: `repo`
  - Then: `git push https://TOKEN@github.com/808dave-rgb/where-to-watch-the-game.git main`
- [ ] Option B: Set up SSH key (see DEPLOYMENT_GUIDE.md)

- [ ] Code pushed successfully

### Step 4: Enable GitHub Pages
- [ ] Go to: https://github.com/808dave-rgb/where-to-watch-the-game/settings/pages
- [ ] Source: `main` branch
- [ ] Folder: `/ (root)`
- [ ] Click **Save**
- [ ] Wait 2-3 minutes

- [ ] GitHub Pages enabled

### Step 5: Verify Deployment
- [ ] Visit: https://808dave-rgb.github.io/where-to-watch-the-game
- [ ] Landing page loads
- [ ] Map displays correctly
- [ ] All 3 city cards show
- [ ] Click "Explore Denver Bars" → works
- [ ] Click "Explore Vegas Bars" → works
- [ ] Click "Explore OC Bars" → works

## Testing Checklist

### Landing Page
- [ ] Map loads with 3 city markers
- [ ] Clicking marker zooms to city
- [ ] City cards display stats correctly
- [ ] Links to city pages work
- [ ] Mobile responsive (test on phone)

### Denver Page
- [ ] Page loads, shows 138 bars
- [ ] Search box filters results
- [ ] Sport checkboxes filter bars
- [ ] Stats bar shows correct counts
- [ ] Bar cards display all info
- [ ] Phone numbers are clickable (tel: links)
- [ ] Website links open in new tab

### Las Vegas Page
- [ ] Page loads, shows 61 bars
- [ ] All filters work
- [ ] Data displays correctly

### Orange County Page
- [ ] Page loads, shows 80 bars
- [ ] All filters work
- [ ] Data displays correctly

### Mobile Testing
- [ ] Test on iPhone/Android
- [ ] Sidebar collapses properly
- [ ] Touch scrolling works
- [ ] Buttons are tap-friendly
- [ ] Text is readable

## Post-Deployment

### Share Your Site
- [ ] Post to Reddit (r/Denver, r/LasVegas, r/OrangeCounty)
- [ ] Share on Twitter/X
- [ ] Post in sports fan groups
- [ ] Share with friends

### Monitor
- [ ] Check GitHub Actions for build status
- [ ] Wait 24h for GitHub Insights to populate
- [ ] Monitor for issues/feedback

### Optional Improvements
- [ ] Add more cities (Phase 2)
- [ ] Collect user feedback
- [ ] Add geocoding for city page maps
- [ ] Add bar photos
- [ ] Custom domain (if desired)

## Troubleshooting

### Site Not Loading
- [ ] Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
- [ ] Check Settings → Pages shows green checkmark
- [ ] Check Actions tab for build errors
- [ ] Wait full 5 minutes after enabling Pages

### Authentication Issues
- [ ] See DEPLOYMENT_GUIDE.md → Step 3
- [ ] Use Personal Access Token method
- [ ] Or set up SSH keys

### Data Not Showing
- [ ] Check browser console for errors (F12)
- [ ] Verify JSON files are in `/data/` folder
- [ ] Check file paths in HTML (should be `../data/city.json`)

## Quick Commands Reference

```bash
# Navigate to project
cd /data/.openclaw/workspace/where-to-watch-the-game

# Check status
git status

# View commit history
git log --oneline

# Test locally
python3 -m http.server 8000
# Visit http://localhost:8000

# Deploy updates (after making changes)
./deploy.sh
```

## Success Indicators

You'll know it worked when:
- ✅ Site loads at GitHub Pages URL
- ✅ All pages are accessible
- ✅ Data displays correctly
- ✅ Search and filters work
- ✅ Mobile version looks good
- ✅ Friends can access and use it

## 🎉 Completion

When all checkboxes above are checked, your site is:
- ✅ **LIVE**
- ✅ **FUNCTIONAL**
- ✅ **SHARED**

Congratulations! You've successfully deployed a multi-city sports bar directory! 🍻🏈⚾🏒🏀

---

## Next Actions

1. **Immediate:** Get feedback from users
2. **Short-term:** Fix any reported issues
3. **Medium-term:** Add more cities
4. **Long-term:** Consider Phase 2 features (reviews, photos, etc.)

## Need Help?

- **Quick answers:** See QUICK_START.md
- **Detailed help:** See DEPLOYMENT_GUIDE.md
- **GitHub issues:** https://github.com/808dave-rgb/where-to-watch-the-game/issues

---

**Ready to go live? Start with Step 1! 🚀**
