@echo off
echo 🚀 Starting AquaGuard AI from project root...
cd /d "c:\tempp\projects\imagine cup\AquaGuard-AI"
echo Current directory: %CD%
echo.
echo 📊 Testing main application...
python app/main.py
echo.
echo 🌐 Testing web application...
python app/web_app.py
echo.
echo ✅ Tests completed from project root!
pause
