"""
Base scraper class for Augips framework
"""

from abc import ABC, abstractmethod
import os
import sys
import traceback
import pandas as pd
from typing import List, Dict, Any, Optional

# Import debug utilities if available
try:
    from ..utils import debug_print
except ImportError:
    # Fallback if debug_print is not available
    def debug_print(message, obj=None, error=None):
        print(f"[DEBUG] {message}")
        if obj is not None:
            print(f"[DEBUG] {obj}")
        if error is not None:
            print(f"[DEBUG] Error: {str(error)}")
            print(f"[DEBUG] Error type: {type(error)}")
            traceback.print_exc(file=sys.stdout)


class Scraper(ABC):
    """Base scraper class that all scrapers should inherit from"""
    
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.output_file = f"data/{company_name.lower().replace(' ', '_')}_locations.csv"
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Main scraping method to be implemented by subclasses
        
        Returns:
            List of dictionaries containing store location data
        """
        pass
    
    def geocode_address(self, address: str) -> tuple:
        """
        Geocode an address to get latitude and longitude
        
        Args:
            address: Full address string
            
        Returns:
            Tuple of (latitude, longitude)
        """
        # Placeholder for geocoding implementation
        # In a real implementation, this would use a geocoding service
        return (0.0, 0.0)
    
    def save_to_csv(self, data: List[Dict[str, Any]]) -> None:
        """
        Save scraped data to CSV
        
        Args:
            data: List of dictionaries containing store location data
        """
        if not data:
            print(f"No data to save for {self.company_name}")
            return
            
        df = pd.DataFrame(data)
        df.to_csv(self.output_file, index=False)
        print(f"Saved {len(data)} locations to {self.output_file}")
    
    def run(self) -> None:
        """Run the scraper and save results"""
        print(f"Scraping {self.company_name} store locations...")
        try:
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            
            # Run the scraper
            debug_print(f"Starting scraper for {self.company_name}")
            data = self.scrape()
            debug_print(f"Scraper returned {len(data)} locations")
            
            # Save the results
            self.save_to_csv(data)
            print(f"Finished scraping {self.company_name}")
            return data
        except Exception as e:
            debug_print(f"Error running scraper for {self.company_name}", error=e)
            print(f"Error: {str(e)}")
            return []