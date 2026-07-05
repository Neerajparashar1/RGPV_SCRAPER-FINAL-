@echo off
title RGPV Result Scraper Launcher
color 0E

echo ===================================================
echo   RGPV Result Scraper - Launcher
echo ===================================================
echo.

:: 1. Determine which Python to use
call ".\find_venv_python.bat"
if "%VENV1_PYTHON_FOUND%"=="1" (
    echo [INFO] Using virtual environment [venv1]...
    goto PYTHON_CHECK_DONE
)

REM Check if global python works and has flask installed
python -c "import flask" >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    echo [INFO] Using system Python [global]...
    goto PYTHON_CHECK_DONE
)

:PYTHON_CHECK_DONE
if "%PYTHON_EXE%"=="" (
    color 0C
    echo [ERROR] No suitable Python environment was found!
    echo.
    echo Please run the "setup.bat" file first to automatically
    echo configure and install all required dependencies.
    echo.
    pause
    exit /b
)

:: 2. Check if app.py exists
if not exist "app.py" (
    color 0C
    echo [ERROR] app.py was not found in this folder!
    echo Please make sure this script is running inside the rgpv_scrapper folder.
    echo.
    pause
    exit /b
)

:: 3. Start the web browser
echo [INFO] Launching your web browser to http://127.0.0.1:5001...
start "" "http://127.0.0.1:5001"
echo.

:: 4. Start the Flask Server
echo [INFO] Starting Flask Server on port 5001...
echo.
"%PYTHON_EXE%" app.py

:: If Flask crashes or exits, pause so the user can read the error message
echo.
echo Server has stopped.
pause
