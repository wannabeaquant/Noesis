#!/usr/bin/env python3
"""
Test script for the geocoding service
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.utils.geocoding import GeocodingService

def test_geocoding():
    """Test the geocoding service with known coordinates"""
    geocoding = GeocodingService()
    
    # Test coordinates for major cities
    test_coordinates = [
        (28.6139, 77.2090, "New Delhi, India"),
        (40.7128, -74.0060, "New York, USA"),
        (51.5074, -0.1278, "London, UK"),
        (48.8566, 2.3522, "Paris, France"),
        (35.6762, 139.6503, "Tokyo, Japan")
    ]
    
    print("🧪 Testing Geocoding Service")
    print("=" * 50)
    
    for lat, lng, expected in test_coordinates:
        print(f"\n📍 Testing coordinates: ({lat}, {lng})")
        print(f"   Expected: {expected}")
        
        place_name = geocoding.get_place_name(lat, lng)
        print(f"   Result: {place_name}")
        
        if place_name and place_name != "Unknown Location":
            print("   ✅ Success!")
        else:
            print("   ❌ Failed or returned unknown location")
        
        # Rate limiting - wait 1 second between requests
        import time
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Geocoding test completed!")

if __name__ == "__main__":
    test_geocoding() 