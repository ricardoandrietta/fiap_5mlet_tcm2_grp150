"""
Configuration settings for the Rental Price Prediction API
"""

import os
from pathlib import Path

# API Configuration
API_TITLE = "Rental Price Prediction API"
API_DESCRIPTION = "API for predicting rental property prices using machine learning"
API_VERSION = "1.0.0"
API_HOST = "0.0.0.0"
API_PORT = 8000

# Model Configuration
MODEL_PATH = Path("trained_model/random_forest_rental_price_model_v1_31.pkl")
EXPECTED_FEATURES = 165

# Default Coordinates (Vancouver, BC)
DEFAULT_LONGITUDE = -123.1207
DEFAULT_LATITUDE = 49.2827

# Default Values for Missing Data
DEFAULT_VALUES = {
    'neighborhood': 'unknown',
    'student_friendly': 0,
    'building_amenity': None,
    'verified_state_machine': 'approved',
    'listing_utility': None,
    'price_frequency': 'monthly',
    'price_monthly': 0.0
}

# Categorical Columns for Preprocessing
CATEGORICAL_COLUMNS = [
    'neighborhood', 'city', 'state', 'building_type_txt_id',
    'verified_state_machine', 'lease_type', 'rental_type', 'price_frequency'
]

# Original Training Data Columns (based on the original code)
ORIGINAL_TRAINING_COLUMNS = [
    'longitude', 'latitude', 'neighborhood', 'city', 'state',
    'building_type_txt_id', 'student_friendly', 'building_amenity',
    'total_rooms', 'total_bathrooms', 'size', 'verified_state_machine',
    'allow_pets', 'allow_smoking', 'furnished', 'count_private_parking',
    'lease_type', 'rental_type', 'listing_utility', 'price_frequency',
    'price_monthly'
]

# Environment Variables
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
