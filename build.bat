@echo off
title RGPV Scraper - EXE Builder
color 0A

echo.
echo =====================================================
echo     RGPV Result Scraper - EXE Builder
echo =====================================================
echo.

:: Check if .venv1 exists
call ".\find_venv_python.bat"
if not "%VENV1_PYTHON_FOUND%"=="1" (
    color 0C
    echo [ERROR] .venv1 virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

:: Check if PyInstaller is available, install if not
"%PYTHON_EXE%" -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing PyInstaller...
    .venv1\Scripts\pip.exe install pyinstaller
)

:: Clean previous build
echo [STEP 1/3] Cleaning previous build...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist\RGPV_Scraper.exe" del /f /q "dist\RGPV_Scraper.exe" 2>nul
echo [DONE] Clean complete.
echo.

:: Run PyInstaller
echo [STEP 2/3] Building EXE (please wait 5-10 minutes)...
echo [INFO] Do NOT close this window.
echo.

"%PYTHON_EXE%" -m PyInstaller build_exe.spec --noconfirm

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERROR] Build FAILED! Check errors above.
    pause
    exit /b 1
)

:: Verify output
echo.
echo [STEP 3/3] Verifying output...
if not exist "dist\RGPV_Scraper.exe" (
    color 0C
    echo [ERROR] dist\RGPV_Scraper.exe not found!
    pause
    exit /b 1
)

color 0A
echo.
echo =====================================================
echo           BUILD SUCCESSFUL!
echo =====================================================
echo.
echo Output: dist\RGPV_Scraper.exe
echo.
echo Send this file to any Windows user who has Edge.
echo (Edge is pre-installed on Windows 10/11)
echo.
echo Press any key to test the EXE now...
pause
start "" "dist\RGPV_Scraper.exe"
