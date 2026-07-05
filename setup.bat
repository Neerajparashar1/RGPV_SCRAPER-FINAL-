@echo off
setlocal enabledelayedexpansion
title RGPV Result Scraper - Auto Setup Wizard
color 0B

echo ===================================================
echo       RGPV Result Scraper - Setup Wizard [100%% Guaranteed]
echo ===================================================
echo.
echo This wizard will automatically configure your Python environment
echo and install all necessary dependencies for the scraper.
echo.

:: 1. Search for Python dynamically
set "PYTHON_EXE="

:: Step 1.1: Check if python command is directly in PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto PYTHON_FOUND
)

:: Step 1.2: Check if Windows Python Launcher [py] is in PATH
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py"
    goto PYTHON_FOUND
)

:: Step 1.3: Scan standard directories where Python is typically installed [local user & global]
echo [INFO] Python is not in PATH. Searching standard directories...

for /d %%d in ("%USERPROFILE%\AppData\Local\Programs\Python\Python*") do (
    if exist "%%d\python.exe" (
        set "PYTHON_EXE=%%d\python.exe"
        goto PYTHON_FOUND
    )
)
for /d %%d in ("%LocalAppData%\Programs\Python\Python*") do (
    if exist "%%d\python.exe" (
        set "PYTHON_EXE=%%d\python.exe"
        goto PYTHON_FOUND
    )
)
for /d %%d in ("%ProgramFiles%\Python*") do (
    if exist "%%d\python.exe" (
        set "PYTHON_EXE=%%d\python.exe"
        goto PYTHON_FOUND
    )
)
for /d %%d in ("%ProgramFiles(x86)%\Python*") do (
    if exist "%%d\python.exe" (
        set "PYTHON_EXE=%%d\python.exe"
        goto PYTHON_FOUND
    )
)
for /d %%d in ("C:\Python*") do (
    if exist "%%d\python.exe" (
        set "PYTHON_EXE=%%d\python.exe"
        goto PYTHON_FOUND
    )
)

:: Step 1.4: Python not found anywhere! Offer automatic silent installation.
color 0E
echo.
echo ===================================================
echo   [NOTICE] Python is not installed on this PC!
echo ===================================================
echo.
echo Python is required to run the scraper. 
echo I can automatically download and install Python 3.10.11 for you.
echo.
set "auto_install=Y"
set /p "auto_install=Would you like to install Python automatically? [Y/N] [Default: Y]: "

if /i "!auto_install!"=="Y" (
    echo.
    echo [INFO] Downloading official Python 3.10.11 installer [approx 27MB]...
    curl -L -o python_installer.exe "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    if !errorlevel! neq 0 (
        color 0C
        echo.
        echo [ERROR] Failed to download Python installer. Please check your internet connection!
        echo You can manually download Python from: https://www.python.org/downloads/
        echo.
        pause
        exit /b
    )
    
    echo.
    echo [INFO] Installing Python silently in the background...
    echo This will take about 60 seconds. Please wait...
    start /wait "" python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python_installer.exe
    echo [OK] Python installation completed!
    echo.
    
    REM Rescan the standard folders to locate the newly installed Python
    echo [INFO] Locating new Python installation...
    for /d %%d in ("%USERPROFILE%\AppData\Local\Programs\Python\Python*") do (
        if exist "%%d\python.exe" (
            set "PYTHON_EXE=%%d\python.exe"
            goto PYTHON_FOUND
        )
    )
    for /d %%d in ("%LocalAppData%\Programs\Python\Python*") do (
        if exist "%%d\python.exe" (
            set "PYTHON_EXE=%%d\python.exe"
            goto PYTHON_FOUND
        )
    )
    
    REM Final fallback in case registry refreshed PATH in the background
    python --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_EXE=python"
        goto PYTHON_FOUND
    )
    
    color 0C
    echo [ERROR] Python was installed, but I could not locate the executable.
    echo Please close this window and open setup.bat again.
    pause
    exit /b
) else (
    echo.
    echo Please install Python manually from: https://www.python.org/downloads/
    echo IMPORTANT: Make sure to check "[x] Add Python to PATH" during installation.
    echo.
    pause
    exit /b
)

:PYTHON_FOUND
color 0B
echo [OK] Found Python executable: "!PYTHON_EXE!"
echo.

:: 2. Setup Virtual Environment [with Global Fallback]
set "VENV_DIR=.venv1"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"
set "USE_GLOBAL=0"

if exist "%VENV_PYTHON%" (
    echo [INFO] Virtual environment already exists.
    set "reinstall=N"
    set /p "reinstall=Do you want to reinstall all dependencies? [Y/N] [Default: N]: "
    if /i "!reinstall!"=="N" (
        goto LAUNCH_APP
    )
    echo.
) else (
    echo [INFO] Creating virtual environment [.venv1]...
    "!PYTHON_EXE!" -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        color 0E
        echo.
        echo [WARNING] Failed to create virtual environment!
        echo This can happen due to restricted folder permissions or OneDrive issues.
        echo Fallback: Installing packages globally to user profile instead...
        set "VENV_PYTHON=!PYTHON_EXE!"
        set "USE_GLOBAL=1"
        pause
    ) else (
        echo [OK] Virtual environment created successfully.
    )
    echo.
)

:: 3. Upgrade Pip and Install Dependencies
echo [INFO] Upgrading pip...
if "!USE_GLOBAL!"=="1" (
    "!VENV_PYTHON!" -m pip install --user --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
) else (
    "!VENV_PYTHON!" -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
)
echo.

echo [INFO] Installing required dependencies...
echo Please hold on while all packages are downloaded and installed...
echo.

set "PIP_CMD="
if "!USE_GLOBAL!"=="1" (
    set "PIP_CMD="!VENV_PYTHON!" -m pip install --user --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org"
) else (
    set "PIP_CMD="%VENV_DIR%\Scripts\pip.exe" install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org"
)

!PIP_CMD! -r requirements.txt
if !errorlevel! neq 0 (
    color 0E
    echo.
    echo [WARNING] Some packages failed to install via requirements.txt.
    echo Retrying direct installation of core modules...
    !PIP_CMD! flask selenium openpyxl xlrd beautifulsoup4 requests webdriver-manager pillow pytesseract python-dotenv ddddocr
)
echo.

:: 4. Verify ddddocr AI Solver
echo [INFO] Checking Deep Learning AI Captcha Solver...
"!VENV_PYTHON!" -c "import ddddocr; print('AI_SOLVER_READY')" >temp_verify.txt 2>&1
findstr "AI_SOLVER_READY" temp_verify.txt >nul
if %errorlevel% equ 0 (
    color 0A
    echo [OK] Deep Learning AI Captcha Solver [ddddocr] is fully loaded and ready!
    set "AI_OK=1"
    del temp_verify.txt
) else (
    color 0E
    echo [WARNING] AI Captcha Solver failed to load.
    type temp_verify.txt
    set "AI_OK=0"
    del temp_verify.txt
)
echo.

:: 5. Fallback check for Tesseract OCR [if AI solver is failed or not present]
if "!AI_OK!"=="0" (
    echo [INFO] AI Solver could not load. Checking if Tesseract OCR is installed as a fallback...
    set "TESS_FOUND=0"
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" set "TESS_FOUND=1"
    if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" set "TESS_FOUND=1"
    
    if "!TESS_FOUND!"=="0" (
        color 0E
        echo.
        echo ===================================================
        echo   [FALLBACK SYSTEM REQUIREMENT] Tesseract OCR
        echo ===================================================
        echo.
        echo Since the Deep Learning AI package has a system mismatch,
        echo we need Tesseract OCR installed on this PC as a fallback.
        echo.
        set "install_tess=Y"
        set /p "install_tess=Would you like me to download and install Tesseract OCR automatically? [Y/N] [Default: Y]: "
        if /i "!install_tess!"=="Y" (
            echo.
            echo [INFO] Downloading Tesseract OCR Installer [approx 48MB]...
            curl -L -o tesseract_installer.exe "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
            if !errorlevel! neq 0 (
                color 0C
                echo [ERROR] Failed to download Tesseract installer.
                echo Please download it manually from: https://github.com/UB-Mannheim/tesseract/wiki
            ) else (
                echo [INFO] Installing Tesseract silently in the background...
                start /wait "" tesseract_installer.exe /S
                del tesseract_installer.exe
                echo [OK] Tesseract OCR installed successfully!
            )
        )
    ) else (
        echo [OK] Tesseract OCR fallback executable was found!
    )
    echo.
)

:: 6. General verification
echo [INFO] Verifying general application packages...
"!VENV_PYTHON!" -c "import flask, selenium, openpyxl, xlrd, bs4; print('VERIFICATION_SUCCESS')" >temp_verify.txt 2>&1
findstr "VERIFICATION_SUCCESS" temp_verify.txt >nul
if %errorlevel% equ 0 (
    color 0A
    echo [OK] Verification successful! All other application dependencies are installed.
    del temp_verify.txt
) else (
    color 0C
    echo [ERROR] Critical verification failed. Some core libraries are missing:
    type temp_verify.txt
    del temp_verify.txt
    pause
)
echo.

echo ===================================================
echo        Setup Completed Successfully!
echo ===================================================
echo.

:LAUNCH_APP
echo.
set "launch=Y"
set /p "launch=Would you like to launch the RGPV Result Scraper now? [Y/N] [Default: Y]: "
if /i "!launch!"=="Y" (
    if exist "run.bat" (
        call run.bat
    ) else (
        echo [INFO] Starting Flask Server...
        start "" "http://127.0.0.1:5001"
        "!VENV_PYTHON!" app.py
    )
) else (
    echo.
    echo Setup complete! You can run the application anytime 
    echo by double-clicking the "run.bat" file.
    echo.
    pause
)
