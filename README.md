# Augips

A modular web scraping framework for extracting automotive store location data from various company websites.

## Features

- Extract store location data from static HTML, interactive maps, and dynamic JS content
- Support for multiple scraping methods (Playwright, Selenium, requests/BeautifulSoup)
- Geocoding fallback for missing coordinates
- Structured CSV output
- Modular and reusable architecture

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from augips.runner import run_scraper

# Run a specific scraper
run_scraper("autozone")

# Run the O'Reilly Auto Parts scraper
run_scraper("oreilly")

# Run simpler static HTML scrapers
run_scraper("advanced")
run_scraper("pepboys")
run_scraper("napa")

# Run international/non-automotive scrapers
run_scraper("ikea")
run_scraper("openstreetmap")
run_scraper("wikipedia")

# Run a test scraper that always works
run_scraper("simple")

# Run all scrapers
run_scraper("all")

# Run with debug mode
run_scraper("autozone", debug=True)
```

### Command Line

```bash
# Run a specific scraper
python main.py autozone

# Run the O'Reilly Auto Parts scraper
python main.py oreilly

# Run simpler static HTML scrapers
python main.py advanced
python main.py pepboys
python main.py napa

# Run international/non-automotive scrapers
python main.py ikea
python main.py openstreetmap
python main.py wikipedia

# Run a test scraper that always works
python main.py simple

# Run with debug mode
python main.py oreilly --debug

# List available scrapers
python main.py list
```

### Troubleshooting

#### Timeout Errors

If you encounter timeout errors with Playwright-based scrapers:

```bash
# Try the simple test scraper first
python main.py simple

# Try static HTML scrapers that don't use Playwright
python main.py advanced
python main.py pepboys
python main.py napa

# Try international/non-automotive scrapers
python main.py ikea
python main.py openstreetmap
python main.py wikipedia

# Use the debug runner for more detailed output
python debug_run.py simple
```

#### 403 Forbidden Errors

Many automotive parts websites block web scraping attempts with 403 Forbidden errors. The scrapers include fallback sample data for demonstration purposes. In a production environment, you might need to:

1. Use rotating proxies
2. Add more sophisticated headers
3. Implement request throttling
4. Consider using their official APIs if available

## Adding New Scrapers

1. Create a new Python file in the `augips/scrapers` directory
2. Implement the `Scraper` class interface
3. Register your scraper in `augips/scrapers/__init__.py`