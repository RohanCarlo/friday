@echo off
title FRIDAY - AI Assistant

:: Wait for system to fully load
echo Waiting for system to fully load...
timeout /t 20 /nobreak

:: Wait for Google Drive to mount
:checkdrive
if not exist "G:\friday\main.py" (
    echo Waiting for Google Drive...
    timeout /t 5 /nobreak
    goto checkdrive
)

:: Start FRIDAY using exact Python path
echo Starting FRIDAY...
"C:\Users\admin\AppData\Local\Programs\Python\Python312\python.exe" "G:\friday\main.py"
pause