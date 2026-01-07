#!/usr/bin/env python3
"""
Test fixed flood prediction module
"""

import os
import sys
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.flood_prediction import FloodPredictor

def test_flood_prediction():
    """Test the fixed flood prediction module"""
    print("🔍 TESTING FIXED FLOOD PREDICTION")
    
    try:
        model = FloodPredictor()
        print("✅ FloodPredictor initialized")
        
        sample_data = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'TEST_001',
            'location_name': 'Test Location',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'rainfall_mm_per_hour': 25.5,
            'river_level_meters': 7.2,
            'soil_moisture_percent': 85.0,
            'temperature_celsius': 22.0,
            'wind_speed_kmh': 15.0,
            'atmospheric_pressure_hpa': 1010.0
        }
        
        result = model.predict_flood_risk(sample_data)
        print("✅ Flood prediction test successful")
        print(f"Risk level: {result.get('risk_level', 'Unknown')}")
        print(f"Confidence: {result.get('confidence_score', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flood prediction test failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_flood_prediction()
    print(f"\n{'✅ FLOOD PREDICTION FIXED' if success else '❌ ISSUES REMAIN'}")
    exit(0 if success else 1)
