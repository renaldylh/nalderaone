@echo off
echo ========================================================
echo Starting Nalderaone Studio Production Server on Windows
echo ========================================================

:: 1. Activate virtual environment
if not exist .venv (
    echo Error: .venv folder not found! Please run 'python -m venv .venv' and install requirements first.
    pause
    exit /b
)
call .venv\Scripts\activate

:: 2. Ensure Waitress is installed (Windows production WSGI server)
pip show waitress >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing waitress WSGI server for Windows production...
    pip install waitress
)

:: 3. Launch background worker in a separate command window
echo Launching Background Task Worker (YouTube publishing)...
start cmd /k "title Nalderaone Worker && .venv\Scripts\activate && python manage.py process_tasks"

:: 4. Launch Production WSGI Server
set PORT=4000
echo Launching Web Server on http://127.0.0.1:%PORT% ...
echo Close this window to stop the server.
waitress-serve --port=%PORT% config.wsgi:application
