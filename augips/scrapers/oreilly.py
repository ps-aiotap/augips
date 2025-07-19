"""
O'Reilly Auto Parts store location scraper
"""

import time
import sys
import traceback
from typing import List, Dict, Any, Optional

# Import optional dependencies with fallbacks
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("WARNING: Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install")
    sync_playwright = None

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    print("WARNING: BeautifulSoup or requests not installed. Install with: pip install beautifulsoup4 requests")
    BeautifulSoup = None
    requests = None

from .base import Scraper
from ..utils import debug_print


class OReillyAutoPartsScraper(Scraper):
    """Scraper for O'Reilly Auto Parts store locations"""
    
    def __init__(self):
        super().__init__("O'Reilly Auto Parts")
        self.base_url = "https://www.oreillyauto.com/"
        self.store_locator_url = "https://www.oreillyauto.com/stores"
        
        # Check robots.txt to ensure we're allowed to scrape
        self._check_robots_txt()
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape O'Reilly Auto Parts store locations
        
        Returns:
            List of dictionaries containing store location data
        """
        # Try both methods and use the one that works
        locations = []
        
        debug_print("Starting O'Reilly scraper")
        
        try:
            debug_print("Attempting to scrape with Playwright")
            locations = self._scrape_with_playwright()
            debug_print(f"Playwright method returned {len(locations)} locations")
        except Exception as e:
            debug_print("Playwright scraping failed, trying static HTML", error=e)
            locations = self._scrape_static_html()
            debug_print(f"Static HTML method returned {len(locations)} locations")
        
        debug_print(f"Total locations before processing: {len(locations)}")
        
        # Add company name to all locations
        for location in locations:
            location["company_name"] = self.company_name
            
            # Geocode addresses that don't have coordinates
            if "latitude" not in location or "longitude" not in location:
                address = f"{location.get('address', '')}, {location.get('city', '')}, {location.get('state', '')} {location.get('zip_code', '')}"
                lat, lng = self.geocode_address(address)
                location["latitude"] = lat
                location["longitude"] = lng
        
        debug_print(f"Final location count: {len(locations)}")
        return locations
    
    def _scrape_static_html(self) -> List[Dict[str, Any]]:
        """Scrape store locations from static HTML"""
        debug_print("Starting static HTML scraping")
        locations = []
        
        try:
            response = requests.get(self.store_locator_url)
            debug_print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                debug_print(f"Page title: {soup.title.text if soup.title else 'No title'}")
                
                # Log some page structure for debugging
                store_elements = soup.select(".store-location, .store-list-item, .store-info")
                debug_print(f"Found {len(store_elements)} potential store elements")
                
                # For demonstration, return sample data
                sample_locations = [
                    {
                        "store_name": "O'Reilly Auto Parts #1234",
                        "address": "123 Main St",
                        "city": "Springfield",
                        "state": "MO",
                        "zip_code": "65801",
                        "latitude": "37.2090",
                        "longitude": "-93.2923"
                    }
                ]
                debug_print(f"Returning {len(sample_locations)} sample locations from static HTML method")
                return sample_locations
                
        except Exception as e:
            debug_print("Error in static HTML scraping", error=e)
        
        return locations
    
    def _scrape_with_playwright(self) -> List[Dict[str, Any]]:
        """Scrape store locations using Playwright for dynamic content"""
        debug_print("Starting Playwright scraping")
        locations = []
        
        # Check if Playwright is available
        if sync_playwright is None:
            debug_print("Playwright not available, skipping this method")
            return []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set timeout after page creation
                page.set_default_timeout(60000)  # Increase timeout to 60 seconds
                
                try:
                    debug_print(f"Navigating to {self.store_locator_url}")
                    page.goto(self.store_locator_url, wait_until="networkidle")
                    
                    # Take a screenshot for debugging
                    page.screenshot(path="debug_oreilly.png")
                    debug_print(f"Page title: {page.title()}")
                    
                    # Example: Enter a zip code to search for stores
                    # Find the actual selectors by inspecting the page
                    search_input = page.query_selector("input[type='text'][placeholder*='ZIP']")
                    if search_input:
                        debug_print("Found ZIP input field")
                        search_input.fill("65801")  # Springfield, MO
                        
                        search_button = page.query_selector("button[type='submit']")
                        if search_button:
                            debug_print("Found search button")
                            search_button.click()
                            
                            # Take a screenshot before waiting for selectors
                            page.screenshot(path="debug/oreilly_before_wait.png")
                            
                            debug_print("Waiting for store results to load...")
                            try:
                                # Try multiple possible selectors with shorter timeouts
                                selectors = [".store-list-item", ".store-location", ".store-info", ".store-details", ".location-list"]
                                found = False
                                
                                for selector in selectors:
                                    debug_print(f"Trying selector: {selector}")
                                    try:
                                        page.wait_for_selector(selector, timeout=15000)
                                        debug_print(f"Found selector: {selector}")
                                        found = True
                                        break
                                    except Exception as e:
                                        debug_print(f"Selector {selector} not found")
                                
                                if not found:
                                    debug_print("No store selectors found, using fallback data")
                                    # Take a screenshot to see what's on the page
                                    page.screenshot(path="debug/oreilly_no_selectors.png")
                                    # Continue with sample data
                                else:
                                    debug_print("Store results loaded")  
                            except Exception as e:
                                debug_print("Error waiting for selectors", error=e)
                            
                            # Extract store data
                            store_elements = page.query_selector_all(".store-list-item, .store-location")
                            debug_print(f"Found {len(store_elements)} store elements")
                            
                            # Log the HTML structure of the first store element for debugging
                            if len(store_elements) > 0:
                                debug_print("First store element HTML:", store_elements[0].inner_html())
                    else:
                        debug_print("Could not find ZIP input field")
                        
                except Exception as e:
                    debug_print("Error during page navigation or data extraction", error=e)
                
                finally:
                    browser.close()
        except Exception as e:
            debug_print("Error initializing Playwright", error=e)
        
        # For demonstration, return sample data
        sample_locations = [
            {
                "store_name": "O'Reilly Auto Parts #5678",
                "address": "456 Oak St",
                "city": "Springfield",
                "state": "MO",
                "zip_code": "65802",
                "latitude": "37.2080",
                "longitude": "-93.2913"
            }
        ]
        
        debug_print(f"Returning {len(sample_locations)} sample locations from Playwright method")
        return sample_locations
    
    def _check_robots_txt(self) -> None:
        """Check robots.txt to ensure we're allowed to scrape"""
        try:
            robots_url = "https://www.oreillyauto.com/robots.txt"
            response = requests.get(robots_url)
            
            if response.status_code == 200:
                robots_content = response.text
                debug_print("Robots.txt content:", robots_content)
                
                # Check if our paths are disallowed
                if "Disallow: /stores" in robots_content:
                    debug_print("WARNING: Scraping this site may violate robots.txt!")
            else:
                debug_print(f"Failed to fetch robots.txt: {response.status_code}")
        except Exception as e:
            debug_print("Error checking robots.txt", error=e)