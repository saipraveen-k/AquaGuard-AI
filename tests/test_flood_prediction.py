#!/usr/bin/env python3
"""
Test Flood Prediction Module
"""

import sys
import os
import numpy as np
from datetime import datetime
# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_flood_prediction():
    """Test flood prediction module"""
    print('🌊 TESTING FLOOD PREDICTION MODULE')
    
    try:
        from modules.flood_prediction import FloodPredictor
        
        model = FloodPredictor()
        print('✅ Flood predictor initialized')
        
        # Test with sample data
        sample_data = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'FLOOD_TEST_001',
            'location_name': 'Flood Test Location',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'rainfall_mm_per_hour': 25.5,
            'river_level_meters': 7.2,
            'soil_moisture_percent': 85.0,
            'temperature_celsius': 22.0,
            'wind_speed_kmh': 15.0,
            'atmospheric_pressure_hpa': 1010.0
        }
        
        prediction = model.predict_flood_risk(sample_data)
        print('✅ Flood prediction working')
        print(f'   - Risk Level: {prediction.get("risk_level", "ERROR")}')
        print(f'   - Confidence: {prediction.get("confidence_score", "ERROR")}')
        
        return True
        
    except Exception as e:
        print(f'❌ ERROR: {str(e)}')
        return False

if __name__ == '__main__':
    success = test_flood_prediction()
    sys.exit(0 if success else 1)
