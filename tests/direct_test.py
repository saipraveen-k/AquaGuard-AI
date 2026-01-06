#!/usr/bin/env python3
"""
Direct test of core functionality
"""

import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct():
    """Test modules directly"""
    print("🔍 DIRECT MODULE TEST")
    print("=" * 40)
    
    try:
        from modules.flood_prediction import FloodPredictor
        print("✅ FloodPredictor import: SUCCESS")
        
        from modules.ship_emergency import ShipEmergencyDetector
        print("✅ ShipEmergencyDetector import: SUCCESS")
        
        from modules.oil_spill_detection import OilSpillDetector
        print("✅ OilSpillDetector import: SUCCESS")
        
        from modules.digital_twin import DigitalTwinSimulator
        print("✅ DigitalTwinSimulator import: SUCCESS")
        
        from modules.alert_system import AlertManager
        print("✅ AlertManager import: SUCCESS")
        
        from modules.data_generator import DataSimulator
        print("✅ DataSimulator import: SUCCESS")
        
        # Test basic functionality
        print("\n🧪 TESTING BASIC FUNCTIONALITY")
        
        # Test flood prediction
        flood_model = FloodPredictor()
        sample_data = {
            'timestamp': '2026-01-06T23:57:36',
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
        
        prediction = flood_model.predict_flood_risk(sample_data)
        print(f"✅ Flood prediction: {prediction.get('risk_level', 'Unknown')}")
        
        # Test ship emergency
        ship_model = ShipEmergencyDetector()
        ship_data = {
            'timestamp': '2026-01-06T23:57:36',
            'mmsi': '123456789',
            'ship_name': 'Test Vessel',
            'ship_type': 'Cargo Ship',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'speed_knots': 1.5,
            'heading_degrees': 45.0
        }
        
        ship_result = ship_model.detect_emergency(ship_data)
        print(f"✅ Ship emergency detection: {ship_result.get('emergency_status', 'Unknown')}")
        
        # Test oil spill
        spill_model = OilSpillDetector()
        spill_data = {
            'timestamp': '2026-01-06T23:57:36',
            'location_id': 'SPILL_001',
            'location_name': 'Test Spill Site',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'oil',
            'estimated_volume_liters': 5000,
            'weather_conditions': {'wind_speed': 10, 'wave_height': 1.5}
        }
        
        spill_result = spill_model.detect_spill('test_image.jpg', spill_data)
        print(f"✅ Oil spill detection: {spill_result.get('spill_detected', False)}")
        
        print("\n🎯 CORE FUNCTIONALITY: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_direct()
    print(f"\n{'✅ ALL CORE SYSTEMS WORKING' if success else '❌ SYSTEM ISSUES'}")
    exit(0 if success else 1)
