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
python -c "open('config.js','w').write('window.RENTMAN_API_TOKEN=\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3ODA2NjU2OTcsIm1lZGV3ZXJrZXIiOjIzNSwiYWNjb3VudCI6InF0ZWNoIiwiY2xpZW50X3R5cGUiOiJvcGVuYXBpIiwiY2xpZW50Lm5hbWUiOiJvcGVuYXBpIiwiZXhwIjoyMDk2Mjg0ODk3LCJpc3MiOiJ7XCJuYW1lXCI6XCJiYWNrZW5kXCIsXCJ2ZXJzaW9uXCI6XCI0Ljg2My4wLjZcIn0ifQ.Dl8qiPmwVvWOLb21AvhjALe-qtFUty1zS_TTMNYbomI\";')"

echo  Token written to config.js
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8080/rentman-dashboard.html"

echo  Starting proxy - do not close this window!
echo  ================================================
echo.
python rentman-proxy.py
pause
