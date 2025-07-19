"""
Base scraper class for Augips framework
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Any, Optional


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
        data = self.scrape()
        self.save_to_csv(data)
        print(f"Finished scraping {self.company_name}")