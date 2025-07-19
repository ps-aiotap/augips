"""
Scrapers package for Augips framework
"""

from .base import Scraper
from .autozone import AutoZoneScraper
from .oreilly import OReillyAutoPartsScraper
from .simple import SimpleScraper
from .advanced import AdvancedAutoPartsScraper
from .pepboys import PepBoysScraper
from .napa import NAPAScraper
from .ikea import IKEAScraper
from .openstreetmap import OpenStreetMapScraper
from .wikipedia import WikipediaScraper

# Register scrapers here
SCRAPERS = {
    "autozone": AutoZoneScraper,
    "oreilly": OReillyAutoPartsScraper,
    "simple": SimpleScraper,
    "advanced": AdvancedAutoPartsScraper,
    "pepboys": PepBoysScraper,
    "napa": NAPAScraper,
    "ikea": IKEAScraper,
    "openstreetmap": OpenStreetMapScraper,
    "wikipedia": WikipediaScraper,
}