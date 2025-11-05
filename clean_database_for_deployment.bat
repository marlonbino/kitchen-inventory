@echo off
echo ============================================================
echo CLEANING DATABASE FOR DEPLOYMENT
echo ============================================================
echo.
echo This will remove all test data (requisitions and stock movements)
echo while keeping items, categories, and users.
echo.
pause

REM Activate virtual environment
call .\kitchen\Scripts\activate.bat

REM Navigate to backend
cd backend

REM Run the Django management command
python manage.py prepare_for_deployment

echo.
echo ============================================================
echo DATABASE CLEANED SUCCESSFULLY!
echo ============================================================
echo.
echo Your database now contains only:
echo   - Items and Categories
echo   - User accounts
echo.
echo All test requisitions and stock movements have been removed.
echo.
pause

