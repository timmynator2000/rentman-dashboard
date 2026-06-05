@echo off
title Rentman Dashboard
color 0A

echo.
echo  ================================================
echo   Rentman Dashboard - Starting...
echo  ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from https://www.python.org
    echo.
    pause
    exit /b 1
)

:: Open browser after a short delay (gives proxy time to start)
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8080/rentman-dashboard.html"

:: Start the proxy (this stays open)
echo  Proxy running - do not close this window!
echo  Browser will open automatically...
echo.
echo  Press Ctrl+C to stop the server.
echo  ================================================
echo.
python rentman-proxy.py

pause