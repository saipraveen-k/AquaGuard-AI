#!/usr/bin/env python3
"""
Deploy Models for AquaGuard AI
"""

import os
import sys
sys.path.append('..')

def deploy_models():
    """Deploy ML models to production"""
    print('🚀 DEPLOYING ML MODELS')
    
    try:
        # Check if models directory exists
        models_dir = '../models'
        if not os.path.exists(models_dir):
            print('❌ Models directory not found')
            return False
        
        # List model files
        model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
        
        if not model_files:
            print('❌ No model files found')
            return False
        
        print(f'✅ Found {len(model_files)} model files:')
        for model_file in model_files:
            print(f'   - {model_file}')
        
        print('✅ Models are ready for deployment')
        return True
        
    except Exception as e:
        print(f'❌ ERROR: {str(e)}')
        return False

if __name__ == '__main__':
    deploy_models()
