#!/usr/bin/env python3
"""
Debug Oil Spill Detection NumPy Issues
"""

import sys
import numpy as np
from datetime import datetime
sys.path.append('..')  # Add parent directory to path

def debug_numpy_issue():
    print('🔍 DEBUGGING NUMPY ISSUES IN SPILL DETECTION')
    print('=' * 50)
    
    try:
        from modules.oil_spill_detection import OilSpillDetector
        
        # Initialize detector
        detector = OilSpillDetector()
        print('✅ Detector initialized')
        
        # Test with simple data
        test_metadata = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'DEBUG_001',
            'location_name': 'Debug Test',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'oil',
            'estimated_volume_liters': 1000,
            'weather_conditions': {'wind_speed': 10}
        }
        
        # Test feature extraction directly
        print('🔍 Testing feature extraction...')
        features = detector._extract_image_features('test.jpg', test_metadata)
        print(f'Features type: {type(features)}')
        print(f'Features: {features}')
        
        for i, f in enumerate(features):
            print(f'Feature {i}: {f} (type: {type(f)})')
        
        # Test scaling
        print('🔍 Testing scaling...')
        features_scaled = detector.scaler.transform([features])
        print(f'Scaled features: {features_scaled}')
        
        # Test prediction
        print('🔍 Testing prediction...')
        prediction = detector.spill_classifier.predict(features_scaled)[0]
        print(f'Prediction: {prediction} (type: {type(prediction)})')
        
        # Test probabilities
        print('🔍 Testing probabilities...')
        probabilities = detector.spill_classifier.predict_proba(features_scaled)[0]
        print(f'Probabilities: {probabilities} (type: {type(probabilities)})')
        
        for i, p in enumerate(probabilities):
            print(f'Probability {i}: {p} (type: {type(p)})')
        
        print('✅ Debug test completed successfully')
        return True
        
    except Exception as e:
        print(f'❌ ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = debug_numpy_issue()
    sys.exit(0 if success else 1)
