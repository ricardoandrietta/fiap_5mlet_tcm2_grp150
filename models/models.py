"""
Data models for the Rental Price Prediction API
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class RentalPredictionRequest(BaseModel):
    """Request model for rental price prediction"""
    longitude: float = Field(..., description="Longitude coordinate", example=-79.416300)
    latitude: float = Field(..., description="Latitude coordinate", example=43.700110)
    city: str = Field(..., description="City name", example="vancouver")
    state: str = Field(..., description="State abbreviation", example="BC")
    building_type: str = Field(..., description="Type of building", example="highrise")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms", example=2)
    bathrooms: int = Field(..., ge=0, description="Number of bathrooms", example=2)
    size: int = Field(..., gt=0, description="Property size in square meters", example=700)
    allow_pets: bool = Field(..., description="Whether pets are allowed", example=True)
    allow_smoking: bool = Field(..., description="Whether smoking is allowed", example=False)
    furnished: bool = Field(..., description="Whether property is furnished", example=False)
    count_private_parking: int = Field(..., ge=0, description="Number of private parking spaces", example=1)
    lease_type: str = Field(..., description="Type of lease", example="long_term")
    rental_type: str = Field(..., description="Type of rental", example="long_term")

    class Config:
        # This ensures fields appear in the order they are defined in the class
        json_schema_extra = {
            "example": {
                "longitude": -79.416300,
                "latitude": 43.700110,
                "city": "vancouver",
                "state": "BC",
                "building_type": "highrise",
                "bedrooms": 2,
                "bathrooms": 2,
                "size": 700,
                "allow_pets": True,
                "allow_smoking": False,
                "furnished": False,
                "count_private_parking": 1,
                "lease_type": "long_term",
                "rental_type": "long_term"
            }
        }


class RentalPredictionResponse(BaseModel):
    """Response model for rental price prediction"""
    predicted_price: float = Field(..., description="Predicted rental price")
    input_data: Dict[str, Any] = Field(..., description="Processed input data used for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 2500.50,
                "input_data": {
                    "longitude": -79.416300,
                    "latitude": 43.700110,
                    "city": "vancouver",
                    "state": "BC",
                    "building_type": "highrise",
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "size": 700,
                    "allow_pets": True,
                    "allow_smoking": False,
                    "furnished": False,
                    "count_private_parking": 1,
                    "lease_type": "long_term",
                    "rental_type": "long_term"
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="API status")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    
    class Config:
        protected_namespaces = ()


class ApiInfoResponse(BaseModel):
    """API information response model"""
    message: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    docs: str = Field(..., description="Documentation URL")
    health: str = Field(..., description="Health check URL")


# Authentication Models
class User(BaseModel):
    """User model for authentication"""
    username: str = Field(..., description="Username")
    hashed_password: str = Field(..., description="Hashed password")
    is_active: bool = Field(default=True, description="Whether user is active")


class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., description="Username", example="fiap")
    password: str = Field(..., description="Password", example="fiap123")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "fiap",
                "password": "fiap123"
            }
        }


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
