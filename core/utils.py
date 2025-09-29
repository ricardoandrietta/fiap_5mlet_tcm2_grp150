"""
Utility functions for the Rental Price Prediction API
"""

from typing import Tuple
from core.config import DEFAULT_LONGITUDE, DEFAULT_LATITUDE


def get_coordinates(city: str, state: str) -> Tuple[float, float]:
    """
    Get longitude and latitude for a given city and state.
    
    Args:
        city: City name
        state: State abbreviation
        
    Returns:
        Tuple of (longitude, latitude)
        
    Note:
        For now, returns default coordinates for Vancouver, BC. 
        In the future, this should query a database or external API.
    """
    # TODO: Replace with actual coordinate lookup from database
    # For now, returning default coordinates for Vancouver, BC
    return DEFAULT_LONGITUDE, DEFAULT_LATITUDE


def format_price(price: float) -> str:
    """
    Format price for display.
    
    Args:
        price: Price value
        
    Returns:
        Formatted price string
    """
    return f"${price:.2f}"


def validate_model_file(model_path: str) -> bool:
    """
    Validate that the model file exists and is accessible.
    
    Args:
        model_path: Path to the model file
        
    Returns:
        True if model file is valid, False otherwise
    """
    import os
    return os.path.exists(model_path) and os.path.isfile(model_path)
