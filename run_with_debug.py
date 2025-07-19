"""
Run a scraper with debug output
"""

import sys
from augips.runner import run_scraper


if __name__ == "__main__":
    if len(sys.argv) > 1:
        scraper_name = sys.argv[1]
        print(f"Running {scraper_name} scraper with debug mode...")
        run_scraper(scraper_name, debug=True)
    else:
        print("Please specify a scraper name")
        print("Example: python run_with_debug.py oreilly")