"""
Geocoding utilities for Augips framework
"""

import os
from typing import Tuple, Optional
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def geocode_address(address: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Geocode an address to get latitude and longitude
    
    Args:
        address: Full address string
        
    Returns:
        Tuple of (latitude, longitude) or (None, None) if geocoding fails
    """
    try:
        # Initialize geocoder
        geolocator = Nominatim(user_agent="augips")
        
        # Geocode the address
        location = geolocator.geocode(address)
        
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not geocode address: {address}")
            return (None, None)
    except Exception as e:
        print(f"Error geocoding address: {address} - {str(e)}")
        return (None, None)