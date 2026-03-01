# 🚀 Deployment Guide

Complete step-by-step instructions to deploy "Where to Watch the Game" to GitHub Pages.

## Prerequisites

- GitHub account (username: 808dave-rgb)
- Git installed on your system
- Terminal/command line access

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to https://github.com/new
2. Repository name: `where-to-watch-the-game`
3. Description: "Multi-city sports bar directory - Find where to watch your team"
4. Set to **Public** (required for free GitHub Pages)
5. **DO NOT** initialize with README (we have one)
6. Click **Create repository**

### Option B: Via GitHub CLI

```bash
gh repo create where-to-watch-the-game --public --description "Multi-city sports bar directory"
```

## Step 2: Connect Local Repo to GitHub

```bash
cd /data/.openclaw/workspace/where-to-watch-the-game

# Add remote
git remote add origin https://github.com/808dave-rgb/where-to-watch-the-game.git

# Verify remote
git remote -v
```

## Step 3: Initial Commit and Push

```bash
# Check status
git status

# Add all files
git add .

# Commit
git commit -m "Initial commit - Multi-city sports bar directory"

# Push to GitHub
git push -u origin main
```

If you get an authentication error, you'll need to:

### Set up GitHub Authentication

**Option A: Personal Access Token (Recommended)**

1. Go to https://github.com/settings/tokens/new
2. Note: "where-to-watch-the-game deployment"
3. Expiration: 90 days (or longer)
4. Scopes: Select `repo` (full control of private repositories)
5. Click **Generate token**
6. Copy the token (you won't see it again!)

Then push using:
```bash
git push https://TOKEN@github.com/808dave-rgb/where-to-watch-the-game.git main
```

**Option B: SSH Key**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/ssh/new
```

Then change remote to SSH:
```bash
git remote set-url origin git@github.com:808dave-rgb/where-to-watch-the-game.git
git push -u origin main
```

## Step 4: Enable GitHub Pages

1. Go to your repo: https://github.com/808dave-rgb/where-to-watch-the-game
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under **Source**:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 2-3 minutes for deployment

Your site will be live at:
```
https://808dave-rgb.github.io/where-to-watch-the-game
```

## Step 5: Verify Deployment

After 2-3 minutes, visit your site and check:

- [ ] Landing page loads with map
- [ ] All 3 city cards display correctly
- [ ] Denver city page works
- [ ] Las Vegas city page works
- [ ] Orange County city page works
- [ ] Search functionality works
- [ ] Sport filters work
- [ ] Mobile responsive design looks good

## 🔄 Updating the Site

After making changes:

```bash
# Using the deploy script
./deploy.sh

# Or manually
git add .
git commit -m "Description of changes"
git push origin main
```

Changes go live in 1-2 minutes.

## 🐛 Troubleshooting

### "Repository not found" error

```bash
# Check remote URL
git remote -v

# Fix if wrong
git remote set-url origin https://github.com/808dave-rgb/where-to-watch-the-game.git
```

### 404 Error on GitHub Pages

1. Check Settings → Pages → Source is set to `main` branch
2. Wait 5 minutes and try again
3. Check build status in Actions tab
4. Ensure `index.html` is in root directory

### Pages not updating

1. Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Check GitHub Actions for build errors
4. Verify files were pushed: `git log`

### Authentication failed

```bash
# Use token
git push https://TOKEN@github.com/808dave-rgb/where-to-watch-the-game.git main

# Or set up credential helper
git config --global credential.helper store
```

## 📊 Monitoring

### Check Build Status

1. Go to repo → Actions tab
2. See deployment history
3. Click on any run to see details

### View Analytics (after 24h)

1. Settings → Insights
2. Traffic tab
3. See visitor stats

## 🎨 Custom Domain (Optional)

If you want to use a custom domain like `wheretowatchthegame.com`:

1. Buy domain from registrar (Namecheap, Google Domains, etc.)
2. Add DNS records:
   ```
   A    185.199.108.153
   A    185.199.109.153
   A    185.199.110.153
   A    185.199.111.153
   ```
3. In repo Settings → Pages → Custom domain:
   - Enter: `wheretowatchthegame.com`
   - Check "Enforce HTTPS"

## 🔐 Security

### Enable Branch Protection (Optional)

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass

### Dependabot Alerts

Settings → Code security and analysis:
- Enable Dependabot alerts
- Enable Dependabot security updates

## 📱 Testing

### Local Testing

```bash
# Simple HTTP server
python3 -m http.server 8000

# Visit: http://localhost:8000
```

### Mobile Testing

1. Get your local IP: `ifconfig` or `ipconfig`
2. Start server: `python3 -m http.server 8000`
3. On phone, visit: `http://YOUR_IP:8000`

### Browser Testing

Test in:
- Chrome/Chromium
- Firefox
- Safari
- Mobile Safari (iOS)
- Chrome Mobile (Android)

## 🎯 Post-Deployment Checklist

- [ ] Site loads at GitHub Pages URL
- [ ] All pages accessible
- [ ] Data loads correctly
- [ ] Search works
- [ ] Filters work
- [ ] Mobile responsive
- [ ] Links work (back to home, etc.)
- [ ] Share URL with friends for feedback

## 📞 Getting Help

- **GitHub Pages Docs:** https://docs.github.com/pages
- **Git Docs:** https://git-scm.com/doc
- **Repo Issues:** https://github.com/808dave-rgb/where-to-watch-the-game/issues

## 🎉 Success!

Your multi-city sports bar directory is now live! 

Share it with:
- Sports fan communities
- Team subreddits
- Local Facebook groups
- Twitter sports fans

---

**Next Steps:**
- Add more cities (see README.md Roadmap)
- Improve with user feedback
- Share on social media
- Consider adding features from Phase 2
