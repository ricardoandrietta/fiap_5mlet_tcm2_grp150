"""
Rental Price Prediction API - Main Application
"""

from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends, status
import uvicorn

from core.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_HOST, API_PORT
from models.models import (
    RentalPredictionRequest, 
    RentalPredictionResponse, 
    HealthResponse, 
    ApiInfoResponse,
    LoginRequest,
    TokenResponse,
    User
)
from services.ml_service import ml_service
from services.auth_service import auth_service, get_current_active_user


# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url=None,
    openapi_tags=[
        {
            "name": "System",
            "description": "System endpoints for health checks and API information",
        },
        {
            "name": "Authentication", 
            "description": "Authentication endpoints for login and user management",
        },
        {
            "name": "Prediction",
            "description": "Machine learning prediction endpoints",
        },
    ]
)


@app.on_event("startup")
async def startup_event():
    """Load model and pipeline on startup"""
    success = ml_service.load_model()
    if not success:
        print("Warning: Model failed to load. API will not function properly.")


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=ml_service.is_loaded
    )


@app.post("/login", response_model=TokenResponse, tags=["Authentication"])
async def login(login_request: LoginRequest):
    """
    Authenticate user and return access token
    
    This endpoint authenticates a user with username and password,
    and returns a JWT access token for subsequent API calls.
    """
    user = auth_service.authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")


@app.post("/predict", response_model=RentalPredictionResponse, tags=["Prediction"])
async def predict_rental_price(
    request: RentalPredictionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Predict rental price based on property features
    
    This endpoint takes property information and returns a predicted rental price
    using a trained machine learning model. Requires authentication.
    """
    try:
        if not ml_service.is_loaded:
            raise HTTPException(
                status_code=500, 
                detail="Model not loaded. Please check server logs."
            )
        
        # Make prediction using the ML service
        predicted_price = ml_service.predict(request.model_dump())
        
        return RentalPredictionResponse(
            predicted_price=predicted_price,
            input_data=request.model_dump()
        )
        
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/me", response_model=User, tags=["Authentication"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user information
    
    This endpoint returns information about the currently authenticated user.
    """
    return current_user

    
@app.get("/", response_model=ApiInfoResponse, tags=["System"])
async def root():
    """Root endpoint with API information"""
    return ApiInfoResponse(
        message=API_TITLE,
        version=API_VERSION,
        docs="/docs",
        health="/health"
    )

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)