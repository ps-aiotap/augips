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

# Run all scrapers
run_scraper("all")
```

## Adding New Scrapers

1. Create a new Python file in the `augips/scrapers` directory
2. Implement the `Scraper` class interface
3. Register your scraper in `augips/scrapers/__init__.py`