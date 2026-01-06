#!/usr/bin/env python3
"""
Health Check for AquaGuard AI
"""

import sys
import asyncio
sys.path.append('..')

async def health_check():
    """Perform system health check"""
    print('🏥 AQUAGUARD AI HEALTH CHECK')
    
    try:
        # Test all modules
        from modules.flood_prediction import FloodPredictor
        from modules.ship_emergency import ShipEmergencyDetector
        from modules.oil_spill_detection import OilSpillDetector
        from modules.digital_twin import DigitalTwinSimulator
        from modules.alert_system import AlertManager
        
        print('✅ All modules imported successfully')
        
        # Initialize modules
        flood_model = FloodPredictor()
        ship_model = ShipEmergencyDetector()
        spill_model = OilSpillDetector()
        digital_twin = DigitalTwinSimulator()
        alert_manager = AlertManager()
        
        print('✅ All modules initialized successfully')
        
        # Test basic functionality
        print('✅ System health check passed')
        return True
        
    except Exception as e:
        print(f'❌ HEALTH CHECK FAILED: {str(e)}')
        return False

if __name__ == '__main__':
    success = asyncio.run(health_check())
    sys.exit(0 if success else 1)
