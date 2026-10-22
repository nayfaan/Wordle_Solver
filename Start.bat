@echo off
setlocal

cd /d "%~dp0"

set "VENV_PY=venv\Scripts\python.exe"

if exist "%VENV_PY%" goto launch

py -3 --version >nul 2>&1
if not errorlevel 1 (
    set "BOOTSTRAP_PY=py -3"
    goto bootstrap
)
python --version >nul 2>&1
if not errorlevel 1 (
    set "BOOTSTRAP_PY=python"
    goto bootstrap
)
goto no_python

:bootstrap
echo Creating virtual environment...
%BOOTSTRAP_PY% -m venv venv
if not exist "%VENV_PY%" goto venv_failed

"%VENV_PY%" -m pip install --upgrade pip
"%VENV_PY%" -m pip install -r requirements.txt

:launch
"%VENV_PY%" main.py
if errorlevel 1 goto crashed
exit /b 0

:no_python
echo.
echo Python 3 was not found on this PC.
echo Install it from https://www.python.org/downloads/ and tick
echo "Add python.exe to PATH" during setup, then run this again.
echo.
pause
exit /b 1

:venv_failed
echo.
echo Could not create the virtual environment in "%CD%\venv".
echo Delete the venv folder if it exists and try again.
echo.
pause
exit /b 1

:crashed
echo.
echo Wordle Solver exited with an error - see the messages above.
echo.
pause
exit /b 1
