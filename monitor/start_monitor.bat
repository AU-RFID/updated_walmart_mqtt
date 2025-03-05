@echo off
echo Starting the File Monitor in WSL...

REM Launch the Flask app in a new window (non-blocking)
start "" wsl.exe -d Ubuntu-20.04 -e bash -c "cd /mnt/c/Users/labau/Documents/test/monitor && python3 app.py"

REM Wait a few seconds for the app to start
timeout /t 5 /nobreak >nul

REM Open the browser to the correct URL
start "" "http://127.0.0.1:5000/"

pause
