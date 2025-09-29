@echo off
REM Rental Price Prediction API Startup Script for Windows

echo Starting Rental Price Prediction API...
echo ======================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if model file exists
if not exist "trained_model\random_forest_rental_price_model.pkl" (
    echo WARNING: Model file not found at trained_model\random_forest_rental_price_model.pkl
    echo Please ensure the model file is in the correct location.
)

REM Start the API server
echo Starting API server...
echo API will be available at: http://localhost:8000
echo Documentation will be available at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo.

python main.py

pause

