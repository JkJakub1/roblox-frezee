@echo off
setlocal

:: ================================================
:: Elevate script to admin if not already running
:: ================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: ================================================
:: Change working directory to script's location
:: ================================================
pushd "%~dp0"

:: ================================================
:: Clear screen
:: ================================================
cls

:: ================================================
:: Check for Python
:: ================================================
echo Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    pause
    popd
    exit /b 1
)

:: ================================================
:: Check & install required Python modules
:: ================================================
echo Checking for required Python modules (psutil, keyboard)...
python -c "import psutil, keyboard" >nul 2>&1
if %errorlevel% neq 0 (
    echo One or more modules missing. Installing psutil and keyboard...
    python -m pip install psutil keyboard
)

:: ================================================
:: Verify installation
:: ================================================
echo Verifying installation...
python -c "import psutil, keyboard" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Installation failed or modules still missing.
    pause
    popd
    exit /b 1
)

:: ================================================
:: Launch main.py
:: ================================================
echo All required modules are installed.
echo Launching main.py...
cls
python "%~dp0main.py"

:: ================================================
:: Cleanup and exit
:: ================================================
popd
pause
