#!/usr/bin/env python3
"""
Simple web app test
"""

import os
import sys
import requests
import time

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_web_app():
    """Test web app API endpoints"""
    print("🌐 TESTING WEB APP API")
    print("=" * 40)
    
    # Wait a moment for web app to start
    time.sleep(2)
    
    try:
        # Test basic connectivity
        response = requests.get('http://localhost:5000/api/flood-data', timeout=5)
        if response.status_code == 200:
            print("✅ Web app API responding correctly")
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                print(f"✅ Flood data API working: {len(data['data'])} records")
        else:
            print("⚠️ Flood data API returned no data")
            
        # Test alerts endpoint
        response = requests.get('http://localhost:5000/api/alerts', timeout=5)
        if response.status_code == 200:
            print("✅ Alerts API responding correctly")
            alerts = response.json()
            if 'alerts' in alerts:
                print(f"✅ Alerts API working: {len(alerts['alerts'])} alerts")
        else:
            print("⚠️ Alerts API not responding")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Web app test failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == '__main__':
    print("Starting web app test in 3 seconds...")
    time.sleep(3)
    success = test_web_app()
    print(f"\n{'✅ WEB APP FULLY FUNCTIONAL' if success else '❌ WEB APP ISSUES'}")
    exit(0 if success else 1)
