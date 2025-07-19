"""
Main entry point for Augips framework
"""

from augips.runner import run_scraper


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Augips - Automotive store location scraper")
    parser.add_argument("scraper", help="Scraper name or 'all' to run all scrapers")
    args = parser.parse_args()
    
    run_scraper(args.scraper)


if __name__ == "__main__":
    main()