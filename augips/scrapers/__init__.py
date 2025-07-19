"""
Scrapers package for Augips framework
"""

from .base import Scraper
from .autozone import AutoZoneScraper

# Register scrapers here
SCRAPERS = {
    "autozone": AutoZoneScraper,
}