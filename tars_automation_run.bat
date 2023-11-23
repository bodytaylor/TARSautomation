@echo off
setlocal enabledelayedexpansion

:: Change the current directory to the location of the script
cd /d "%~dp0"

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Run the Python script with the provided arguments
python "code\main.py"

:: Deactivate the virtual environment
call pricing_env\Scripts\deactivate.bat
pause