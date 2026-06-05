@echo off
title Rentman Dashboard
color 0A

echo.
echo  ================================================
echo   Rentman Warehouse Dashboard
echo  ================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    pause
    exit /b 1
)

:: Write config.js using Python - edit the token inside this script
python -c "open('config.js','w').write('window.RENTMAN_API_TOKEN=\"1234123123XYZ1234123123XYZ1234123123XYZ1234123123XYZ\";')"

echo  Token written to config.js
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8080/rentman-dashboard.html"

echo  Starting proxy - do not close this window!
echo  ================================================
echo.
python rentman-proxy.py
pause
