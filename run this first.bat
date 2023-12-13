@echo off
echo Setting up virtual environment...

:: Set the path where you want to create the virtual environment
set VENV_FOLDER=.venv

:: Check if the virtual environment folder already exists
if not exist %VENV_FOLDER% (
    python -m venv %VENV_FOLDER%
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
call %VENV_FOLDER%\Scripts\activate

:: Upgrade pip
echo Upgrade pip
python3 -m pip install --upgrade pip

echo Installing required packages...
:: Install your required packages using pip
pip install -r requirements.txt

echo Setup complete.
pause
