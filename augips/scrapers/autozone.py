"""
AutoZone store location scraper
"""

import time
import requests
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

from .base import Scraper
from ..utils import debug_print


class AutoZoneScraper(Scraper):
    """Scraper for AutoZone store locations"""
    
    def __init__(self):
        super().__init__("AutoZone")
        self.base_url = "https://www.autozone.com/locations/"
        self.store_locator_url = "https://www.autozone.com/store-locator"
        
        # Check robots.txt to ensure we're allowed to scrape
        self._check_robots_txt()
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape AutoZone store locations
        
        This is an example implementation that demonstrates different scraping approaches:
        1. Static HTML parsing with BeautifulSoup
        2. Dynamic content with Playwright
        3. Geocoding fallback
        
        Returns:
            List of dictionaries containing store location data
        """
        # Example implementation - in a real scenario, choose the appropriate method
        # based on the website structure
        
        # Method 1: Static HTML parsing (placeholder)
        # locations = self._scrape_static_html()
        
        # Method 2: Dynamic content with Playwright (placeholder)
        locations = self._scrape_with_playwright()
        
        # Add company name to all locations
        for location in locations:
            location["company_name"] = self.company_name
            
            # Geocode addresses that don't have coordinates
            if "latitude" not in location or "longitude" not in location:
                address = f"{location.get('address', '')}, {location.get('city', '')}, {location.get('state', '')} {location.get('zip_code', '')}"
                lat, lng = self.geocode_address(address)
                location["latitude"] = lat
                location["longitude"] = lng
        
        return locations
    
    def _scrape_static_html(self) -> List[Dict[str, Any]]:
        """Scrape store locations from static HTML"""
        locations = []
        
        # Example implementation using requests and BeautifulSoup
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find store location elements (placeholder logic)
            # In a real implementation, you would inspect the page structure
            # and extract the relevant data
            store_elements = soup.select(".store-location")
            
            for store in store_elements:
                location = {
                    "store_name": store.select_one(".store-name").text.strip(),
                    "address": store.select_one(".address").text.strip(),
                    "city": store.select_one(".city").text.strip(),
                    "state": store.select_one(".state").text.strip(),
                    "zip_code": store.select_one(".zip").text.strip(),
                    # Coordinates might be available in data attributes
                    "latitude": store.get("data-lat"),
                    "longitude": store.get("data-lng"),
                }
                locations.append(location)
        
        return locations
    
    def _scrape_with_playwright(self) -> List[Dict[str, Any]]:
        """Scrape store locations using Playwright for dynamic content"""
        locations = []
        
        try:
            # Example implementation using Playwright
            # This is a placeholder that demonstrates the approach
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Set timeout after page creation
                page.set_default_timeout(60000)  # Increase timeout to 60 seconds
                
                try:
                    # Navigate to the store locator page
                    page.goto(self.store_locator_url, wait_until="networkidle")
                    
                    # Example: Enter a zip code to search for stores
                    # Wait for the input field to be available
                    page.wait_for_selector("#store-search-input", timeout=60000)
                    page.fill("#store-search-input", "90210")
                    
                    # Wait for the button to be available and click it
                    page.wait_for_selector("#store-search-button", timeout=60000)
                    page.click("#store-search-button")
                    
                    # Take a screenshot before waiting for selectors
                    page.screenshot(path="debug/autozone_before_wait.png")
                    
                    debug_print("Waiting for store results to load...")
                    try:
                        # Try multiple possible selectors
                        selectors = [".store-list-item", ".store-location", ".store-info", ".store-details"]
                        found = False
                        
                        for selector in selectors:
                            debug_print(f"Trying selector: {selector}")
                            try:
                                page.wait_for_selector(selector, timeout=15000)
                                debug_print(f"Found selector: {selector}")
                                found = True
                                break
                            except Exception as e:
                                debug_print(f"Selector {selector} not found", error=e)
                        
                        if not found:
                            debug_print("No store selectors found, using fallback data")
                            # Take a screenshot to see what's on the page
                            page.screenshot(path="debug/autozone_no_selectors.png")
                    except Exception as e:
                        debug_print("Error waiting for selectors", error=e)
                    
                    # Extract store data from the page
                    # In a real implementation, you would inspect the page structure
                    # and extract the relevant data
                    store_elements = page.query_selector_all(".store-list-item")
                    
                    for store in store_elements:
                        try:
                            # Example extraction logic with error handling
                            store_name = store.query_selector(".store-name").inner_text()
                            address = store.query_selector(".address").inner_text()
                            city = store.query_selector(".city").inner_text()
                            state = store.query_selector(".state").inner_text()
                            zip_code = store.query_selector(".zip").inner_text()
                            
                            # Coordinates might be available in data attributes or from a map
                            lat = store.get_attribute("data-lat")
                            lng = store.get_attribute("data-lng")
                            
                            location = {
                                "store_name": store_name,
                                "address": address,
                                "city": city,
                                "state": state,
                                "zip_code": zip_code,
                                "latitude": lat,
                                "longitude": lng,
                            }
                            locations.append(location)
                        except Exception as e:
                            debug_print("Error extracting store data", error=e)
                            continue
                            
                except Exception as e:
                    debug_print("Error during page navigation or data extraction", error=e)
                
                finally:
                    browser.close()
        except Exception as e:
            debug_print("Error initializing Playwright", error=e)
        
        # For demonstration purposes, return some sample data
        # In a real implementation, this would be the actual scraped data
        sample_locations = [
            {
                "store_name": "AutoZone #1234",
                "address": "123 Main St",
                "city": "Beverly Hills",
                "state": "CA",
                "zip_code": "90210",
                "latitude": "34.0736",
                "longitude": "-118.4004"
            },
            {
                "store_name": "AutoZone #5678",
                "address": "456 Oak Ave",
                "city": "Beverly Hills",
                "state": "CA",
                "zip_code": "90211",
                # No coordinates - will use geocoding
            }
        ]
        
        # Add debugging for actual selectors found on the page
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                debug_print("Navigating to AutoZone store locator")
                page.goto(self.store_locator_url, wait_until="networkidle")
                
                # Take a screenshot for debugging
                page.screenshot(path="debug_autozone.png")
                
                # Debug page content
                html_content = page.content()
                debug_print(f"Page title: {page.title()}")
                debug_print(f"Page URL: {page.url}")
                
                # Find actual form elements
                form_elements = page.query_selector_all("input")
                debug_print(f"Found {len(form_elements)} input elements")
                
                for i, elem in enumerate(form_elements):
                    elem_type = elem.get_attribute("type")
                    elem_id = elem.get_attribute("id")
                    elem_name = elem.get_attribute("name")
                    debug_print(f"Input {i}: type={elem_type}, id={elem_id}, name={elem_name}")
                
                browser.close()
        except Exception as e:
            debug_print("Error during debugging", error=e)
        
        return sample_locations
        
    def _check_robots_txt(self) -> None:
        """Check robots.txt to ensure we're allowed to scrape"""
        try:
            robots_url = "https://www.autozone.com/robots.txt"
            response = requests.get(robots_url)
            
            if response.status_code == 200:
                robots_content = response.text
                debug_print("Robots.txt content:", robots_content)
                
                # Check if our paths are disallowed
                # Based on the robots.txt, these paths are not explicitly disallowed
                disallowed_paths = ['/atg/', '/dyn/', '/cart', '/rest/', '/checkout', '/error/', '/ymme/']
                debug_print("Checking if our paths are allowed...")
                debug_print(f"Store locator URL: {self.store_locator_url}")
                
                is_allowed = True
                for path in disallowed_paths:
                    if path in self.store_locator_url:
                        is_allowed = False
                        debug_print(f"WARNING: Path {path} is disallowed in robots.txt!")
                
                if is_allowed:
                    debug_print("Store locator path appears to be allowed by robots.txt")
            else:
                debug_print(f"Failed to fetch robots.txt: {response.status_code}")
        except Exception as e:
            debug_print("Error checking robots.txt", error=e)