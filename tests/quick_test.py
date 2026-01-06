#!/usr/bin/env python3
"""
Quick test runner for AquaGuard AI from project root
"""

import os
import sys
import subprocess

def main():
    print('🚀 QUICK TEST FROM PROJECT ROOT')
    print(f'Current directory: {os.getcwd()}')
    
    # Test main app
    try:
        result = subprocess.run([sys.executable, 'app/main.py'], 
                              capture_output=True, text=True)
        print('✅ app/main.py executed successfully')
        print('STDOUT:', result.stdout)
        if result.stderr:
            print('STDERR:', result.stderr)
    except Exception as e:
        print(f'❌ Error running app/main.py: {e}')
    
    # Test web app
    try:
        result = subprocess.run([sys.executable, 'app/web_app.py'], 
                              capture_output=True, text=True)
        print('✅ app/web_app.py executed successfully')
        print('STDOUT:', result.stdout)
        if result.stderr:
            print('STDERR:', result.stderr)
    except Exception as e:
        print(f'❌ Error running app/web_app.py: {e}')

if __name__ == '__main__':
    main()
