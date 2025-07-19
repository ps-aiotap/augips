"""
Simple test scraper that always works
"""

from typing import List, Dict, Any

from .base import Scraper
from ..utils import debug_print


class SimpleScraper(Scraper):
    """A simple test scraper that always works"""
    
    def __init__(self):
        super().__init__("Simple Test")
        debug_print("Simple scraper initialized")
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Return sample data without any web requests
        
        Returns:
            List of dictionaries containing sample store location data
        """
        debug_print("Simple scraper running")
        
        # Create sample data
        locations = [
            {
                "store_name": "Test Store #1",
                "address": "123 Test St",
                "city": "Testville",
                "state": "TS",
                "zip_code": "12345",
                "latitude": "35.1234",
                "longitude": "-90.5678",
                "company_name": self.company_name
            },
            {
                "store_name": "Test Store #2",
                "address": "456 Sample Ave",
                "city": "Exampleburg",
                "state": "TS",
                "zip_code": "67890",
                "latitude": "36.5678",
                "longitude": "-91.1234",
                "company_name": self.company_name
            }
        ]
        
        debug_print(f"Simple scraper returning {len(locations)} locations")
        return locations