#!/usr/bin/env python3
"""
Test oil spill detection module loading and functionality
"""

import os
import sys
from datetime import datetime

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.oil_spill_detection import OilSpillDetector

def test_oil_spill_detection():
    """Test the oil spill detection module"""
    print("🔍 TESTING OIL SPILL DETECTION MODULE")
    
    try:
        # Initialize the detector
        detector = OilSpillDetector()
        print("✅ OilSpillDetector initialized successfully")
        
        # Test with sample data
        sample_metadata = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'SPILL_001',
            'location_name': 'Test Spill Site',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'oil',
            'estimated_volume_liters': 5000,
            'weather_conditions': {'wind_speed': 10, 'wave_height': 1.5}
        }
        
        # Test detection
        result = detector.detect_spill('test_image.jpg', sample_metadata)
        print("✅ Oil spill detection test successful")
        print(f"Spill detected: {result.get('spill_detected', False)}")
        print(f"Spill type: {result.get('spill_type', 'None')}")
        print(f"Confidence: {result.get('confidence_score', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Oil spill detection test failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_oil_spill_detection()
    print(f"\n{'✅ OIL SPILL DETECTION WORKING' if success else '❌ OIL SPILL DETECTION ISSUES'}")
    exit(0 if success else 1)
