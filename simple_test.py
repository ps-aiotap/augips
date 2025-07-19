"""
Very simple test script that just runs the simple scraper
"""

from augips.scrapers import SimpleScraper

print("Starting simple test...")

# Create and run the simple scraper
scraper = SimpleScraper()
locations = scraper.scrape()

print(f"Found {len(locations)} locations")

if locations:
    print("\nFirst location:")
    for key, value in locations[0].items():
        print(f"  {key}: {value}")

print("\nTest complete!")