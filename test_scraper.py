"""
Simple test script for scrapers
"""

import sys
from augips.scrapers import SCRAPERS
from augips.utils import debug_print


def test_scraper(scraper_name):
    """Test a specific scraper"""
    print(f"Testing {scraper_name} scraper...")
    
    if scraper_name not in SCRAPERS:
        print(f"Scraper '{scraper_name}' not found. Available scrapers: {', '.join(SCRAPERS.keys())}")
        return
    
    try:
        # Initialize the scraper
        scraper_class = SCRAPERS[scraper_name]
        scraper = scraper_class()
        
        # Run the scraper
        print(f"Initialized {scraper_name} scraper for {scraper.company_name}")
        print(f"Output file will be: {scraper.output_file}")
        
        # Test the scrape method directly
        print("Testing scrape method...")
        locations = scraper.scrape()
        print(f"Scrape method returned {len(locations)} locations")
        
        # Print the first location
        if locations:
            print("\nFirst location data:")
            for key, value in locations[0].items():
                print(f"  {key}: {value}")
        else:
            print("No locations returned")
            
    except Exception as e:
        debug_print(f"Error testing {scraper_name} scraper", error=e)
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_scraper(sys.argv[1])
    else:
        print("Please specify a scraper name")
        print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")