@echo off
setlocal
cd /d "%~dp0\..\.."
if not exist "local-data\sniffer-venv\Scripts\python.exe" (
  py -3 -m venv local-data\sniffer-venv
  if errorlevel 1 goto failed
)
local-data\sniffer-venv\Scripts\python.exe -m pip install -r scripts\airtime-sniffer\requirements.txt
if errorlevel 1 goto failed
local-data\sniffer-venv\Scripts\python.exe scripts\airtime-sniffer\sniffer.py --gui %*
if errorlevel 1 goto failed
exit /b 0
:failed
echo Sniffer startup failed. Check Python 3.10+ and the error above.
pause
exit /b 1
