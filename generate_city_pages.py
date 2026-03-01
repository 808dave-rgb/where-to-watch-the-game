#!/usr/bin/env python3
"""
Generate city-specific HTML pages from template
"""
from pathlib import Path

# City configuration
CITIES = {
    'denver': {
        'name': 'Denver',
        'emoji': '🏔️',
        'slug': 'denver'
    },
    'las-vegas': {
        'name': 'Las Vegas',
        'emoji': '🎰',
        'slug': 'las-vegas'
    },
    'orange-county': {
        'name': 'Orange County',
        'emoji': '🌊',
        'slug': 'orange-county'
    }
}

def main():
    template_path = Path('/data/.openclaw/workspace/where-to-watch-the-game/city_template.html')
    output_dir = Path('/data/.openclaw/workspace/where-to-watch-the-game/cities')
    output_dir.mkdir(exist_ok=True)
    
    # Read template
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate page for each city
    for slug, config in CITIES.items():
        # Replace placeholders
        page = template.replace('{{CITY_NAME}}', config['name'])
        page = page.replace('{{CITY_EMOJI}}', config['emoji'])
        page = page.replace('{{CITY_SLUG}}', config['slug'])
        
        # Write output
        output_path = output_dir / f"{slug}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(page)
        
        print(f"✅ Generated {output_path}")

if __name__ == '__main__':
    main()
