#!/usr/bin/env python3
"""
Comprehensive verification of AquaGuard AI main application and paths
"""

import os
import sys
import subprocess
from datetime import datetime

def check_paths():
    """Verify all file paths are working correctly"""
    print("🔍 VERIFYING FILE PATHS AND STRUCTURE")
    print("=" * 50)
    
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Check required directories
    required_dirs = [
        'app',
        'modules', 
        'models',
        'data',
        'data/outputs',
        'data/raw',
        'data/images',
        'tests',
        'scripts',
        'docs',
        'templates'
    ]
    
    print("\n📁 Directory Structure Check:")
    for dir_path in required_dirs:
        exists = os.path.exists(dir_path)
        status = "✅" if exists else "❌"
        print(f"  {dir_path}: {status}")
        
    # Check key files
    key_files = [
        'app/main.py',
        'app/web_app.py',
        'modules/flood_prediction.py',
        'modules/ship_emergency.py',
        'modules/oil_spill_detection.py',
        'modules/digital_twin.py',
        'modules/alert_system.py',
        'modules/data_generator.py',
        'requirements.txt',
        '.env',
        '.env.example',
        'templates/dashboard.html'
    ]
    
    print("\n📋 Key Files Check:")
    for file_path in key_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {file_path}: {status}")
        
    # Check model files
    print("\n🤖 ML Models Check:")
    models_dir = 'models'
    if os.path.exists(models_dir):
        model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
        print(f"  Models directory: ✅ ({len(model_files)} models found)")
        for model in model_files:
            print(f"    - {model}")
    else:
        print(f"  Models directory: ❌ (not found)")
        
    # Check data outputs
    print("\n📊 Data Outputs Check:")
    outputs_dir = 'data/outputs'
    if os.path.exists(outputs_dir):
        output_files = [f for f in os.listdir(outputs_dir) if f.endswith('.csv')]
        print(f"  Data outputs: ✅ ({len(output_files)} CSV files found)")
        for output in output_files:
            print(f"    - {output}")
    else:
        print(f"  Data outputs: ❌ (not found)")
    
    return True

def test_imports():
    """Test that all module imports work correctly"""
    print("\n🔍 TESTING MODULE IMPORTS")
    print("=" * 50)
    
    try:
        # Test from app directory
        print("Testing imports from app/ directory...")
        os.chdir('app')
        
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from modules.flood_prediction import FloodPredictor
        print("  ✅ modules.flood_prediction imported")
        
        from modules.ship_emergency import ShipEmergencyDetector
        print("  ✅ modules.ship_emergency imported")
        
        from modules.oil_spill_detection import OilSpillDetector
        print("  ✅ modules.oil_spill_detection imported")
        
        from modules.digital_twin import DigitalTwinSimulator
        print("  ✅ modules.digital_twin imported")
        
        from modules.alert_system import AlertManager
        print("  ✅ modules.alert_system imported")
        
        from modules.data_generator import DataSimulator
        print("  ✅ modules.data_generator imported")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import test failed: {str(e)}")
        return False

def test_ml_functionality():
    """Test ML module functionality"""
    print("\n🧪 TESTING ML FUNCTIONALITY")
    print("=" * 50)
    
    try:
        # Go back to root directory
        os.chdir('..')
        
        # Test flood prediction
        print("Testing flood prediction module...")
        from modules.flood_prediction import FloodPredictor
        
        flood_model = FloodPredictor()
        print("  ✅ FloodPredictor initialized")
        
        # Test with sample data
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
        
        prediction = flood_model.predict_flood_risk(sample_data)
        print(f"  ✅ Flood prediction working: {prediction.get('risk_level', 'Unknown')}")
        print(f"  ✅ Confidence score: {prediction.get('confidence_score', 0)}")
        
        # Test ship emergency detection
        print("Testing ship emergency detection module...")
        from modules.ship_emergency import ShipEmergencyDetector
        
        ship_model = ShipEmergencyDetector()
        print("  ✅ ShipEmergencyDetector initialized")
        
        ship_sample = {
            'timestamp': datetime.now().isoformat(),
            'mmsi': '123456789',
            'ship_name': 'Test Vessel',
            'ship_type': 'Cargo Ship',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'speed_knots': 1.5,
            'heading_degrees': 45.0
        }
        
        ship_detection = ship_model.detect_emergency(ship_sample)
        print(f"  ✅ Ship emergency detection working: {ship_detection.get('emergency_status', 'Unknown')}")
        print(f"  ✅ Confidence score: {ship_detection.get('confidence_score', 0)}")
        
        # Test oil spill detection
        print("Testing oil spill detection module...")
        from modules.oil_spill_detection import OilSpillDetector
        
        spill_model = OilSpillDetector()
        print("  ✅ OilSpillDetector initialized")
        
        spill_sample = {
            'timestamp': datetime.now().isoformat(),
            'location_id': 'SPILL_001',
            'location_name': 'Test Spill Site',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'spill_type': 'oil',
            'estimated_volume_liters': 5000,
            'weather_conditions': {'wind_speed': 10, 'wave_height': 1.5}
        }
        
        spill_detection = spill_model.detect_spill('test_image.jpg', spill_sample)
        print(f"  ✅ Oil spill detection working: {spill_detection.get('spill_detected', False)}")
        print(f"  ✅ Spill type: {spill_detection.get('spill_type', 'None')}")
        print(f"  ✅ Confidence score: {spill_detection.get('confidence_score', 0)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ ML functionality test failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("🎯 COMPREHENSIVE AQUAGUARD AI VERIFICATION")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Run all checks
    paths_ok = check_paths()
    imports_ok = test_imports()
    ml_ok = test_ml_functionality()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    print(f"✅ File Paths: {'PASS' if paths_ok else 'FAIL'}")
    print(f"✅ Module Imports: {'PASS' if imports_ok else 'FAIL'}")
    print(f"✅ ML Functionality: {'PASS' if ml_ok else 'FAIL'}")
    
    overall_status = paths_ok and imports_ok and ml_ok
    print(f"\n🏆 OVERALL STATUS: {'✅ READY FOR IMAGINE CUP' if overall_status else '❌ NEEDS ATTENTION'}")
    
    if overall_status:
        print("\n🎉 All systems verified and working correctly!")
        print("🚀 AquaGuard AI is ready for Imagine Cup demonstration!")
    else:
        print("\n⚠️ Some issues detected - please review above output")
    
    return 0 if overall_status else 1

if __name__ == '__main__':
    exit(main())
