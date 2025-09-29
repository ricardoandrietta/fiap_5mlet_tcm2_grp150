"""
Machine Learning service for rental price prediction
"""

import joblib
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from pathlib import Path

from core.config import (
    MODEL_PATH, EXPECTED_FEATURES, DEFAULT_VALUES, 
    CATEGORICAL_COLUMNS, ORIGINAL_TRAINING_COLUMNS
)
from core.utils import get_coordinates


class MLService:
    """Machine Learning service for handling model operations"""
    
    def __init__(self):
        self.model: Optional[Any] = None
        self.is_loaded = False
    
    def load_model(self) -> bool:
        """
        Load the trained machine learning model.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not MODEL_PATH.exists():
                print(f"Model file not found at {MODEL_PATH}")
                return False
            
            self.model = joblib.load(MODEL_PATH)
            self.is_loaded = True
            print("Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.is_loaded = False
            return False
    
    def preprocess_data(self, request_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess input data for prediction.
        
        Args:
            request_data: Input data from API request
            
        Returns:
            Preprocessed DataFrame ready for prediction
        """
        # Get coordinates for the city/state
        longitude, latitude = get_coordinates(request_data['city'], request_data['state'])
        
        # Create DataFrame with the input data
        new_data_sample = pd.DataFrame({
            'longitude': [longitude],
            'latitude': [latitude],
            'neighborhood': [DEFAULT_VALUES['neighborhood']],
            'city': [request_data['city'].lower()],
            'state': [request_data['state'].upper()],
            'building_type_txt_id': [request_data['building_type']],
            'student_friendly': [DEFAULT_VALUES['student_friendly']],
            'building_amenity': [DEFAULT_VALUES['building_amenity']],
            'total_rooms': [float(request_data['bedrooms'])],
            'total_bathrooms': [float(request_data['bathrooms'])],
            'size': [float(request_data['size'])],
            'verified_state_machine': [DEFAULT_VALUES['verified_state_machine']],
            'allow_pets': [1 if request_data['allow_pets'] else 0],
            'allow_smoking': [1.0 if request_data['allow_smoking'] else 0.0],
            'furnished': [1.0 if request_data['furnished'] else 0.0],
            'count_private_parking': [float(request_data['count_private_parking'])],
            'lease_type': [request_data['lease_type']],
            'rental_type': [request_data['rental_type']],
            'listing_utility': [DEFAULT_VALUES['listing_utility']],
            'price_frequency': [DEFAULT_VALUES['price_frequency']],
            'price_monthly': [DEFAULT_VALUES['price_monthly']]
        })
        
        # Ensure columns match the original training data
        new_data_sample = new_data_sample.reindex(columns=ORIGINAL_TRAINING_COLUMNS, fill_value=np.nan)
        
        # Apply preprocessing pipeline
        new_data_sample_prepared = self._apply_preprocessing(new_data_sample)
        
        return new_data_sample_prepared
    
    def _apply_preprocessing(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply preprocessing transformations to the data.
        
        Args:
            data: Raw input DataFrame
            
        Returns:
            Preprocessed DataFrame with expected number of features
        """
        # Create a copy for preprocessing
        processed_data = data.copy()
        
        # Handle categorical variables with one-hot encoding
        for col in CATEGORICAL_COLUMNS:
            if col in processed_data.columns:
                # Create dummy variables for each category
                dummies = pd.get_dummies(processed_data[col], prefix=col)
                processed_data = pd.concat([processed_data, dummies], axis=1)
                processed_data = processed_data.drop(col, axis=1)
        
        # Fill any remaining NaN values with 0
        processed_data = processed_data.fillna(0)
        
        # Ensure all columns are numeric
        for col in processed_data.columns:
            processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce').fillna(0)
        
        # Adjust feature count to match expected features
        processed_data = self._adjust_feature_count(processed_data)
        
        return processed_data
    
    def _adjust_feature_count(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Adjust the number of features to match the expected count.
        
        Args:
            data: DataFrame with current features
            
        Returns:
            DataFrame with adjusted feature count
        """
        current_features = data.shape[1]
        
        if current_features < EXPECTED_FEATURES:
            # Add zero columns to match expected feature count
            missing_features = EXPECTED_FEATURES - current_features
            zero_columns = pd.DataFrame(
                np.zeros((data.shape[0], missing_features)),
                columns=[f'feature_{i}' for i in range(missing_features)],
                index=data.index
            )
            data = pd.concat([data, zero_columns], axis=1)
            
        elif current_features > EXPECTED_FEATURES:
            # Truncate if we have too many features
            data = data.iloc[:, :EXPECTED_FEATURES]
        
        return data
    
    def predict(self, request_data: Dict[str, Any]) -> float:
        """
        Make a price prediction for the given input data.
        
        Args:
            request_data: Input data from API request
            
        Returns:
            Predicted rental price
            
        Raises:
            RuntimeError: If model is not loaded
            Exception: If prediction fails
        """
        if not self.is_loaded or self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Preprocess the data
        processed_data = self.preprocess_data(request_data)
        
        # Make prediction
        predicted_price = self.model.predict(processed_data)
        
        return float(predicted_price[0])


# Global ML service instance
ml_service = MLService()
