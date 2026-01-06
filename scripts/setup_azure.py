#!/usr/bin/env python3
"""
Setup Azure Services for AquaGuard AI
"""

import os
from dotenv import load_dotenv

def setup_azure():
    """Setup Azure environment variables"""
    print('🔧 SETTING UP AZURE SERVICES')
    
    # Load existing .env file
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_KEY',
        'AZURE_OPENAI_DEPLOYMENT_NAME',
        'AZURE_COMPUTER_VISION_ENDPOINT',
        'AZURE_COMPUTER_VISION_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print('❌ MISSING ENVIRONMENT VARIABLES:')
        for var in missing_vars:
            print(f'   - {var}')
        print('\nPlease set these in your .env file')
        return False
    else:
        print('✅ All Azure environment variables are set')
        return True

if __name__ == '__main__':
    setup_azure()
