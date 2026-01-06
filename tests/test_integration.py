#!/usr/bin/env python3
"""
Integration Test for AquaGuard AI
Tests all modules working together
"""

import sys
import os
import asyncio
from datetime import datetime
# Add project root to path for app imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_integration():
    """Test full system integration"""
    print('🔗 TESTING AQUAGUARD AI INTEGRATION')
    
    try:
        from app.main import AquaGuardAI
        
        # Initialize system
        aquaguard = AquaGuardAI()
        print('✅ System initialized')
        
        # Run simulation cycle
        await aquaguard.run_simulation_cycle()
        print('✅ Simulation cycle completed')
        
        # Get status
        status = aquaguard.get_current_status()
        print(f'✅ System status: {status.get("system_status", "ERROR")}')
        
        return True
        
    except Exception as e:
        print(f'❌ ERROR: {str(e)}')
        return False

if __name__ == '__main__':
    success = asyncio.run(test_integration())
    sys.exit(0 if success else 1)
