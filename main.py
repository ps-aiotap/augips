"""
Main entry point for Augips framework
"""

from augips.runner import run_scraper


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Augips - Automotive store location scraper")
    parser.add_argument("scraper", help="Scraper name, 'all' to run all scrapers, or 'list' to show available scrapers")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    if args.scraper.lower() == "list":
        print("Available scrapers:")
        from augips.scrapers import SCRAPERS
        for name in SCRAPERS.keys():
            print(f"- {name}")
    else:
        run_scraper(args.scraper, debug=args.debug)


if __name__ == "__main__":
    main()