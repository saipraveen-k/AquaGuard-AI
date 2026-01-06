#!/usr/bin/env python3
"""
Test Ship Emergency Detection Module
"""

import sys
import numpy as np
from datetime import datetime
sys.path.append('..')

def test_ship_emergency():
    """Test ship emergency detection module"""
    print('🚢 TESTING SHIP EMERGENCY DETECTION MODULE')
    
    try:
        from modules.ship_emergency import ShipEmergencyDetector
        
        model = ShipEmergencyDetector()
        print('✅ Ship emergency detector initialized')
        
        # Test with sample data
        sample_data = {
            'timestamp': datetime.now().isoformat(),
            'mmsi': '123456789',
            'ship_name': 'Test Vessel',
            'ship_type': 'Cargo Ship',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'speed_knots': 1.5,
            'heading_degrees': 45.0
        }
        
        detection = model.detect_emergency(sample_data)
        print('✅ Ship emergency detection working')
        print(f'   - Emergency Status: {detection.get("emergency_status", "ERROR")}')
        print(f'   - Confidence: {detection.get("confidence_score", "ERROR")}')
        
        return True
        
    except Exception as e:
        print(f'❌ ERROR: {str(e)}')
        return False

if __name__ == '__main__':
    success = test_ship_emergency()
    sys.exit(0 if success else 1)
