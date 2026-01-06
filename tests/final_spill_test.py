#!/usr/bin/env python3
"""
Final Oil Spill Detection Test for Imagine Cup
"""

import sys
import numpy as np
from datetime import datetime
sys.path.append('..')  # Add parent directory to path

def final_test():
    print('🏆 FINAL OIL & CHEMICAL SPILL DETECTION TEST')
    print('=' * 50)
    
    try:
        from modules.oil_spill_detection import OilSpillDetector
        
        # Initialize detector
        detector = OilSpillDetector()
        print('✅ Detector initialized successfully')
        
        # Test with high-confidence oil spill
        oil_metadata = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'FINAL_OIL_TEST',
            'location_name': 'Final Oil Test',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'oil',
            'estimated_volume_liters': 10000,  # Large spill
            'weather_conditions': {'wind_speed': 5, 'wave_height': 1.0}
        }
        
        print('🔍 Testing high-confidence oil spill...')
        oil_result = detector.detect_spill('test_oil.jpg', oil_metadata)
        
        print(f'✅ Oil Detection Result:')
        print(f'   - Spill Detected: {oil_result.get("spill_detected", "ERROR")}')
        print(f'   - Spill Type: {oil_result.get("spill_type", "ERROR")}')
        print(f'   - Severity: {oil_result.get("severity_level", "ERROR")}')
        print(f'   - Confidence: {oil_result.get("confidence_score", "ERROR")}')
        print(f'   - Has Explanation: {"detection_explanation" in oil_result}')
        
        # Test with chemical spill
        chem_metadata = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'FINAL_CHEM_TEST',
            'location_name': 'Final Chemical Test',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'chemical',
            'estimated_volume_liters': 5000,
            'weather_conditions': {'wind_speed': 20, 'wave_height': 3.0}
        }
        
        print('\n🔍 Testing chemical spill...')
        chem_result = detector.detect_spill('test_chem.jpg', chem_metadata)
        
        print(f'✅ Chemical Detection Result:')
        print(f'   - Spill Detected: {chem_result.get("spill_detected", "ERROR")}')
        print(f'   - Spill Type: {chem_result.get("spill_type", "ERROR")}')
        print(f'   - Severity: {chem_result.get("severity_level", "ERROR")}')
        print(f'   - Confidence: {chem_result.get("confidence_score", "ERROR")}')
        
        # Test with normal water
        normal_metadata = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'FINAL_NORMAL_TEST',
            'location_name': 'Final Normal Test',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'none',
            'estimated_volume_liters': 0,
            'weather_conditions': {'wind_speed': 10, 'wave_height': 0.5}
        }
        
        print('\n🔍 Testing normal water...')
        normal_result = detector.detect_spill('test_normal.jpg', normal_metadata)
        
        print(f'✅ Normal Detection Result:')
        print(f'   - Spill Detected: {normal_result.get("spill_detected", "ERROR")}')
        print(f'   - Spill Type: {normal_result.get("spill_type", "ERROR")}')
        print(f'   - Confidence: {normal_result.get("confidence_score", "ERROR")}')
        
        # Get model info
        model_info = detector.get_model_info()
        print(f'\n📊 Model Information:')
        print(f'   - Model Type: {model_info.get("model_type", "ERROR")}')
        print(f'   - Validation Accuracy: {model_info.get("validation_accuracy", "ERROR")}')
        print(f'   - Responsible AI: {model_info.get("responsible_ai_compliance", "ERROR")}')
        print(f'   - Confidence Threshold: {model_info.get("confidence_threshold", "ERROR")}')
        
        print('\n🎯 FINAL ASSESSMENT:')
        
        # Check if core functionality works
        core_tests = [
            oil_result.get("spill_detected") is not None,
            chem_result.get("spill_detected") is not None,
            normal_result.get("spill_detected") is not None,
            "detection_explanation" in oil_result,
            "detection_explanation" in chem_result,
            "detection_explanation" in normal_result
        ]
        
        if all(core_tests):
            print('✅ CORE FUNCTIONALITY: WORKING')
        else:
            print('❌ CORE FUNCTIONALITY: ISSUES DETECTED')
        
        # Check responsible AI features
        responsible_ai_tests = [
            model_info.get("confidence_threshold") == 0.65,
            model_info.get("openai_fallback") == True,
            model_info.get("edge_case_handling") == True,
            model_info.get("data_validation") == True
        ]
        
        if all(responsible_ai_tests):
            print('✅ RESPONSIBLE AI: IMPLEMENTED')
        else:
            print('❌ RESPONSIBLE AI: MISSING FEATURES')
        
        # Overall assessment
        if all(core_tests) and all(responsible_ai_tests):
            print('\n🏆 OIL & CHEMICAL SPILL DETECTION: READY FOR IMAGINE CUP')
            return True
        else:
            print('\n⚠️ OIL & CHEMICAL SPILL DETECTION: NEEDS ATTENTION')
            return False
            
    except Exception as e:
        print(f'❌ CRITICAL ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = final_test()
    sys.exit(0 if success else 1)
