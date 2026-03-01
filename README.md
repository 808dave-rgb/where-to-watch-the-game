# 🏈⚾🏒🏀 Where to Watch the Game

**Find your team's bar across Denver, Las Vegas, and Orange County!**

A multi-city sports bar directory with interactive maps, searchable listings, and team-specific information for NFL, MLB, NHL, and NBA games.

## 🌟 Features

- **3 Major Cities:** Denver, Las Vegas, Orange County
- **279+ Sports Bars** across all locations
- **4 Major Leagues:** NFL, MLB, NHL, NBA
- **Interactive Landing Page** with city map
- **Searchable Directories** for each city
- **Filter by Sport** - Find exactly what you need
- **Mobile Responsive** - Works great on all devices
- **Pure Vanilla JS** - No build step required
- **GitHub Pages Ready** - Deploy in minutes

## 📊 Coverage

| City | Total Bars | NFL | MLB | NHL | NBA |
|------|------------|-----|-----|-----|-----|
| 🏔️ Denver | 138 | 77 | 5 | 27 | 29 |
| 🎰 Las Vegas | 61 | 40 | 6 | 9 | 6 |
| 🌊 Orange County | 80 | 30 | 39 | 5 | 6 |

## 🚀 Quick Start

### View Locally

```bash
# Clone the repo
git clone https://github.com/808dave-rgb/where-to-watch-the-game.git
cd where-to-watch-the-game

# Open in browser
open index.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000
```

### Deploy to GitHub Pages

1. **Fork or clone this repo** to your GitHub account
2. **Go to Settings** → Pages
3. **Source:** Deploy from main branch, root directory
4. **Save** and wait 2-3 minutes
5. **Your site is live!** at `https://yourusername.github.io/where-to-watch-the-game`

## 📁 Project Structure

```
where-to-watch-the-game/
├── index.html              # Landing page with map
├── cities/                 # City-specific pages
│   ├── denver.html
│   ├── las-vegas.html
│   └── orange-county.html
├── data/                   # JSON data files
│   ├── denver.json
│   ├── las-vegas.json
│   └── orange-county.json
├── convert_to_json.py      # Script to convert MD → JSON
├── generate_city_pages.py  # Script to generate city pages
├── city_template.html      # Template for city pages
└── README.md
```

## 🔧 Tech Stack

- **HTML/CSS/JavaScript** - Pure vanilla, no frameworks
- **Leaflet.js** - Interactive maps
- **GitHub Pages** - Free hosting
- **JSON** - Structured data storage

### Why Vanilla JS?

- ✅ Zero build time
- ✅ No dependencies to manage
- ✅ Instant deployment
- ✅ Easy to maintain
- ✅ Fast page loads

## 📱 Responsive Design

All pages are fully optimized for:
- 📱 Mobile phones (iOS & Android)
- 💻 Tablets
- 🖥️ Desktop browsers

## 🗺️ Data Format

Each city has a JSON file with this structure:

```json
{
  "city": "denver",
  "total_bars": 138,
  "sports": ["NFL", "NBA", "NHL", "MLB"],
  "bars": [
    {
      "name": "Bar Name",
      "teams": ["Team 1", "Team 2"],
      "address": "123 Main St, Denver, CO",
      "phone": "(303) 555-1234",
      "website": "https://example.com",
      "notes": "Description and details",
      "sports": ["NFL", "MLB"],
      "city": "denver"
    }
  ],
  "by_sport": {
    "NFL": [...],
    "MLB": [...]
  }
}
```

## 🔄 Updating Data

### From Markdown Research

If you have new markdown files with bar research:

```bash
# Place markdown files in /research directory
# Format: city-sport-bars.md (e.g., vegas-nfl-bars.md)

# Run converter
python3 convert_to_json.py

# Data is updated in /data/*.json files
```

### Manual JSON Editing

You can directly edit the JSON files in `/data/` directory.

### Regenerate City Pages

After updating data:

```bash
python3 generate_city_pages.py
```

## 🎨 Customization

### Change Colors

Edit the CSS in `index.html` or city pages:

```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Accent color */
color: #5a67d8;
```

### Add New Cities

1. Add city data to `/data/newcity.json`
2. Add city config to `generate_city_pages.py`
3. Run `python3 generate_city_pages.py`
4. Update `index.html` with new city card

## 📊 Data Sources

Research compiled from:
- Reddit (r/Denver, r/LasVegas, r/OrangeCounty, team subreddits)
- 2ndHomeSports.com
- Fan club directories
- GameWatch.info
- Local sports media
- Google Maps reviews
- Yelp

**Research completed:** February 28 - March 1, 2026

## ⚠️ Disclaimer

Bar information changes frequently:
- Bars may close or relocate
- Team affiliations may change
- Hours and policies vary
- **Always call ahead to confirm**

## 🤝 Contributing

Found a bar we missed? Know of a closure or change?

### Ways to Contribute:

1. **Open an Issue** with bar details
2. **Submit a Pull Request** with updated JSON
3. **Contact:** [Your contact info]

### Contribution Guidelines:

- Include full bar details (name, address, phone, website)
- Specify which teams they show
- Provide source/verification
- Follow existing JSON format

## 📄 License

**Data:** Public domain - freely use, modify, and share  
**Code:** MIT License

## 🙏 Credits

- **Research & Development:** Phil (OpenClaw AI Assistant)
- **Data Collection:** Multi-source verification (Reddit, fan clubs, local media)
- **Community:** Thanks to all the fan clubs and Reddit communities who share this information

## 🔗 Related Projects

- [Denver Sports Bars](https://github.com/808dave-rgb/denver-sports-bars) - Original Denver-only project
- More cities coming soon!

## 📞 Contact

- **GitHub:** [@808dave-rgb](https://github.com/808dave-rgb)
- **Issues:** [Report a problem](https://github.com/808dave-rgb/where-to-watch-the-game/issues)

## 🗺️ Roadmap

### Phase 1: Launch ✅
- [x] 3 cities (Denver, Vegas, OC)
- [x] Landing page with map
- [x] City directory pages
- [x] Search and filter functionality

### Phase 2: Enhancement 🚧
- [ ] Add geocoding for map pins on city pages
- [ ] Team logo images
- [ ] Bar photos
- [ ] User reviews/ratings

### Phase 3: Expansion 📋
- [ ] Phoenix
- [ ] Chicago
- [ ] New York City
- [ ] Nashville
- [ ] More cities based on demand

### Phase 4: Features 💡
- [ ] Mobile app (PWA)
- [ ] User submissions
- [ ] Real-time updates
- [ ] Game day specials
- [ ] Happy hour info

## 🎯 SEO & Discoverability

Keywords: sports bars, NFL bars, MLB bars, NHL bars, NBA bars, team bars, where to watch games, sports bar directory, Denver sports bars, Las Vegas sports bars, Orange County sports bars

---

**Made with 🏈⚾🏒🏀 for sports fans everywhere**

*Last updated: March 1, 2026*
