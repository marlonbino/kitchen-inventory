@echo off
echo ========================================
echo  Backend Setup and Migration Script
echo ========================================
echo.

cd backend

echo Step 1: Checking for virtual environment...
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment found.
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Step 4: Running database migrations...
python manage.py migrate

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. In a new terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.

pause


