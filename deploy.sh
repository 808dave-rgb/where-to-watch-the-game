#!/bin/bash
# Deployment script for GitHub Pages

set -e

echo "🚀 Deploying Where to Watch the Game"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Run: git init"
    exit 1
fi

# Check if remote is configured
if ! git remote get-url origin &> /dev/null; then
    echo "⚠️  No remote configured"
    echo "Add remote with: git remote add origin https://github.com/808dave-rgb/where-to-watch-the-game.git"
    exit 1
fi

# Stage all changes
echo "📦 Staging files..."
git add .

# Commit
echo "💾 Committing..."
read -p "Commit message (default: 'Update site'): " msg
msg=${msg:-"Update site"}
git commit -m "$msg" || echo "No changes to commit"

# Push to GitHub
echo "🌐 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your site will be live at:"
echo "https://808dave-rgb.github.io/where-to-watch-the-game"
echo ""
echo "If this is your first deployment:"
echo "1. Go to: https://github.com/808dave-rgb/where-to-watch-the-game/settings/pages"
echo "2. Source: Deploy from main branch"
echo "3. Save and wait 2-3 minutes"
