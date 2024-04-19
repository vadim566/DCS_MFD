@echo off
setlocal

rem Step 1: Source the virtual environment
call venv\Scripts\activate

rem Step 2: Start the Python scripts in different threads
start "First Script" cmd /c python left_mfd.py
start "Second Script" cmd /c python right_mfd.py

rem Wait for the scripts to finish
timeout /t 10 /nobreak

rem Deactivate the virtual environment
deactivate

endlocal
