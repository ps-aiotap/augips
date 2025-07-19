"""
Runner module for executing scrapers
"""

import os
from typing import Optional, List
from .scrapers import SCRAPERS


def run_scraper(scraper_name: str, debug: bool = False) -> None:
    """
    Run a specific scraper or all scrapers
    
    Args:
        scraper_name: Name of the scraper to run, or "all" to run all scrapers
        debug: Enable debug mode
    """
    # Import debug utilities
    try:
        from .utils import debug_print
    except ImportError:
        # Fallback if debug_print is not available
        def debug_print(message, obj=None, error=None):
            if debug:
                print(f"[DEBUG] {message}")
                if obj is not None:
                    print(f"[DEBUG] {obj}")
                if error is not None:
                    print(f"[DEBUG] Error: {str(error)}")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create debug directory if needed
    if debug:
        os.makedirs("debug", exist_ok=True)
        print("Debug mode enabled - check debug/ directory for screenshots and logs")
    
    debug_print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")
    
    if scraper_name.lower() == "all":
        print(f"Running all {len(SCRAPERS)} scrapers...")
        for name, scraper_class in SCRAPERS.items():
            try:
                debug_print(f"Initializing {name} scraper")
                scraper = scraper_class()
                scraper.run()
            except Exception as e:
                debug_print(f"Error running {name} scraper", error=e)
                print(f"Error running {name} scraper: {str(e)}")
    elif scraper_name.lower() in SCRAPERS:
        print(f"Running {scraper_name} scraper...")
        try:
            debug_print(f"Initializing {scraper_name} scraper")
            scraper = SCRAPERS[scraper_name.lower()]()
            scraper.run()
        except Exception as e:
            debug_print(f"Error running {scraper_name} scraper", error=e)
            print(f"Error running {scraper_name} scraper: {str(e)}")
    else:
        print(f"Scraper '{scraper_name}' not found. Available scrapers: {', '.join(SCRAPERS.keys())}")
        print("\nAvailable scrapers:")
        for name in SCRAPERS.keys():
            print(f"- {name}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        run_scraper(sys.argv[1])
    else:
        print("Please specify a scraper name or 'all'")
        print(f"Available scrapers: {', '.join(SCRAPERS.keys())}")