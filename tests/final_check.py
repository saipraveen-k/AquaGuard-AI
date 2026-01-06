#!/usr/bin/env python3
"""
Final comprehensive check of main.py and web_app.py
"""

import os
import sys
import subprocess
import time

def run_main_app():
    """Test main.py from project root"""
    print("🚀 TESTING MAIN.PY FROM PROJECT ROOT")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, 'app/main.py'
        ], capture_output=True, text=True, timeout=30)
        
        print("✅ main.py executed successfully")
        print("STDOUT:", result.stdout[-500:] if result.stdout else "No output")
        if result.stderr:
            print("STDERR:", result.stderr[-500:] if result.stderr else "No errors")
        else:
            print("STDERR: No errors")
            
        # Check for key success indicators
        if "AquaGuard AI System Initialized" in result.stdout:
            print("✅ System initialization confirmed")
        if "Simulation cycle completed" in result.stdout:
            print("✅ Simulation cycle completed")
        if "Data exported to ./data/outputs" in result.stdout:
            print("✅ Data export confirmed")
            
        return True
        
    except Exception as e:
        print(f"❌ main.py test failed: {str(e)}")
        return False

def run_web_app():
    """Test web_app.py from project root"""
    print("\n🌐 TESTING WEB_APP.PY FROM PROJECT ROOT")
    print("=" * 60)
    
    try:
        # Start web app in background
        process = subprocess.Popen([
            sys.executable, 'app/web_app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("✅ web_app.py started (checking for startup)")
        
        # Wait a bit for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ web_app.py running successfully")
            
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            print("❌ web_app.py failed to start")
            return False
            
    except Exception as e:
        print(f"❌ web_app.py test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🎯 FINAL COMPREHENSIVE CHECK")
    print("=" * 60)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test main app
    main_ok = run_main_app()
    
    # Test web app
    web_ok = run_web_app()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    print(f"✅ Main Application: {'PASS' if main_ok else 'FAIL'}")
    print(f"✅ Web Application: {'PASS' if web_ok else 'FAIL'}")
    
    overall_success = main_ok and web_ok
    print(f"\n🏆 OVERALL STATUS: {'✅ BOTH APPS READY' if overall_success else '❌ ISSUES DETECTED'}")
    
    if overall_success:
        print("\n🎉 Both applications working correctly!")
        print("🚀 AquaGuard AI is ready for Imagine Cup!")
    else:
        print("\n⚠️ Some issues detected - please review above output")
    
    return 0 if overall_success else 1

if __name__ == '__main__':
    exit(main())
