"""
Simplified debug runner that prints all output
"""

import sys
import traceback
from augips.scrapers import SCRAPERS


def main():
    """Run a scraper with full debug output"""
    if len(sys.argv) < 2:
        print("Usage: python debug_run.py [scraper_name]")
        print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")
        return
    
    scraper_name = sys.argv[1].lower()
    
    if scraper_name not in SCRAPERS:
        print(f"Scraper '{scraper_name}' not found")
        print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")
        return
    
    print(f"Running {scraper_name} scraper...")
    
    try:
        # Initialize the scraper
        scraper_class = SCRAPERS[scraper_name]
        scraper = scraper_class()
        
        # Run the scraper
        print(f"Scraping {scraper.company_name} store locations...")
        locations = scraper.scrape()
        
        # Print results
        print(f"Found {len(locations)} locations")
        
        if locations:
            print("\nSample location:")
            for key, value in locations[0].items():
                print(f"  {key}: {value}")
            
            # Save to CSV
            import os
            os.makedirs("data", exist_ok=True)
            
            output_file = f"data/{scraper_name}_locations.csv"
            import pandas as pd
            df = pd.DataFrame(locations)
            df.to_csv(output_file, index=False)
            print(f"\nSaved {len(locations)} locations to {output_file}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()


if __name__ == "__main__":
    main()