@echo off
echo ========================================
echo  Applying Database Migrations
echo ========================================
echo.

cd backend

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found at backend\venv
    echo Please create it with: python -m venv venv
    echo.
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo ========================================
echo  Migration Complete!
echo ========================================
echo.
echo If you see any errors above, please check:
echo 1. Virtual environment is activated
echo 2. All dependencies are installed (pip install -r requirements.txt)
echo 3. Database file is not locked or corrupted
echo.

pause


