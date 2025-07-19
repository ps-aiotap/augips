"""
Wikipedia scraper for extracting location data from lists of places
"""

from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

from .base import Scraper
from ..utils import debug_print, get_request_headers


class WikipediaScraper(Scraper):
    """Scraper for Wikipedia lists of places (very unlikely to be blocked)"""
    
    def __init__(self):
        super().__init__("Wikipedia Places")
        self.base_url = "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States"
        
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape national park locations from Wikipedia
        
        Returns:
            List of dictionaries containing location data
        """
        debug_print("Starting Wikipedia scraper")
        locations = []
        
        try:
            # Use requests and BeautifulSoup for a simpler approach
            headers = get_request_headers()
            debug_print(f"Fetching {self.base_url} with anti-blocking headers")
            response = requests.get(self.base_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                debug_print("Successfully fetched page")
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Log the page title for debugging
                title = soup.title.text if soup.title else "No title"
                debug_print(f"Page title: {title}")
                
                # Find the main table with national parks
                tables = soup.select(".wikitable")
                if tables:
                    debug_print(f"Found {len(tables)} tables")
                    main_table = tables[0]  # First table is usually the main one
                    
                    # Extract rows from the table
                    rows = main_table.select("tr")
                    debug_print(f"Found {len(rows)} rows in the table")
                    
                    # Skip header row
                    for row in rows[1:]:
                        cells = row.select("td")
                        if len(cells) >= 4:  # Ensure we have enough cells
                            try:
                                park_name = cells[0].text.strip()
                                location_cell = cells[2].text.strip()
                                
                                # Parse location (usually in format "state, state")
                                location_parts = location_cell.split(",")
                                city = ""
                                state = location_parts[0].strip() if location_parts else ""
                                
                                # Some entries have coordinates in the table
                                coords = cells[3].text.strip() if len(cells) > 3 else ""
                                lat, lng = "", ""
                                
                                # Very basic coordinate parsing (would need improvement in real implementation)
                                if "°N" in coords and "°W" in coords:
                                    try:
                                        lat_part = coords.split("°N")[0].strip().split()[-1]
                                        lng_part = coords.split("°W")[0].split("°N")[-1].strip()
                                        lat = lat_part
                                        lng = "-" + lng_part  # West is negative
                                    except:
                                        pass
                                
                                location = {
                                    "store_name": park_name,
                                    "address": "",  # National parks don't have street addresses
                                    "city": city,
                                    "state": state,
                                    "zip_code": "",
                                    "latitude": lat,
                                    "longitude": lng,
                                    "company_name": "National Park Service"
                                }
                                locations.append(location)
                            except Exception as e:
                                debug_print(f"Error parsing row: {str(e)}")
                                continue
                
                debug_print(f"Extracted {len(locations)} locations from Wikipedia")
                
                if locations:
                    return locations
            else:
                debug_print(f"Failed to fetch page: {response.status_code}")
                
        except Exception as e:
            debug_print("Error scraping Wikipedia", error=e)
        
        # Fallback data if the scraping fails
        debug_print("Using fallback sample data")
        sample_locations = [
            {
                "store_name": "Yellowstone National Park",
                "address": "",
                "city": "",
                "state": "Wyoming, Montana, Idaho",
                "zip_code": "",
                "latitude": "44.4280",
                "longitude": "-110.5885",
                "company_name": "National Park Service"
            },
            {
                "store_name": "Grand Canyon National Park",
                "address": "",
                "city": "",
                "state": "Arizona",
                "zip_code": "",
                "latitude": "36.1069",
                "longitude": "-112.1129",
                "company_name": "National Park Service"
            },
            {
                "store_name": "Yosemite National Park",
                "address": "",
                "city": "",
                "state": "California",
                "zip_code": "",
                "latitude": "37.8651",
                "longitude": "-119.5383",
                "company_name": "National Park Service"
            }
        ]
        
        debug_print(f"Returning {len(sample_locations)} fallback locations")
        return sample_locations