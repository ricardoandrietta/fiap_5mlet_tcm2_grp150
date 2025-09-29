#!/bin/bash

# Rental Price Prediction API Startup Script

echo "Starting Rental Price Prediction API..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if model file exists
if [ ! -f "trained_model/random_forest_rental_price_model.pkl" ]; then
    echo "WARNING: Model file not found at trained_model/random_forest_rental_price_model.pkl"
    echo "Please ensure the model file is in the correct location."
fi

# Start the API server
echo "Starting API server..."
echo "API will be available at: http://localhost:8000"
echo "Documentation will be available at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

