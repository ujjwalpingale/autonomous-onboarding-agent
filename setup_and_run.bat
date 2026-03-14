@echo off
echo ===================================================
echo Setting up the Autonomous Developer Onboarding Agent
echo ===================================================

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r backend\requirements.txt

echo ===================================================
echo Setup Complete!
echo Please open backend\.env and add your GEMINI_API_KEY.
echo.
echo To run the backend server, use this command:
echo call venv\Scripts\activate.bat ^& cd backend ^& uvicorn main:app --reload
echo ===================================================
pause
