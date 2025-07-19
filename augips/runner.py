"""
Runner module for executing scrapers
"""

import os
from typing import Optional, List
from .scrapers import SCRAPERS


def run_scraper(scraper_name: str) -> None:
    """
    Run a specific scraper or all scrapers
    
    Args:
        scraper_name: Name of the scraper to run, or "all" to run all scrapers
    """
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    if scraper_name.lower() == "all":
        print(f"Running all {len(SCRAPERS)} scrapers...")
        for name, scraper_class in SCRAPERS.items():
            scraper = scraper_class()
            scraper.run()
    elif scraper_name.lower() in SCRAPERS:
        print(f"Running {scraper_name} scraper...")
        scraper = SCRAPERS[scraper_name.lower()]()
        scraper.run()
    else:
        print(f"Scraper '{scraper_name}' not found. Available scrapers: {', '.join(SCRAPERS.keys())}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        run_scraper(sys.argv[1])
    else:
        print("Please specify a scraper name or 'all'")
        print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")