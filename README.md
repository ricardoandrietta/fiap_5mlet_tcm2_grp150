# Rental Price Prediction API

A FastAPI-based REST API for predicting rental property prices using a trained machine learning model.

> **🔐 AUTHENTICATION REQUIRED**: This API uses JWT authentication. Use username `fiap` and password `fiap123` to access protected endpoints.

## 🔐 Quick Start with Authentication

**Default Credentials:**
- **Username**: `fiap`
- **Password**: `fiap123`

**Quick Test:**
1. Start the API: `docker-compose up -d`
2. Open Swagger UI: http://localhost:8000/docs
3. Click "Authorize" (🔒) and login with the credentials above
4. Test the `/predict` endpoint with authentication

## Features

- 🏠 Predict rental prices based on property features
- 🔐 JWT-based authentication system
- 📊 Input validation with Pydantic models
- 📚 Interactive API documentation with Swagger UI
- 🔍 Health check endpoints
- 🚀 Fast and efficient FastAPI framework

## API Endpoints

### Public Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /login` - Authenticate user and get access token

### Protected Endpoints (Require Authentication)
- `POST /predict` - Predict rental price
- `GET /me` - Get current user information

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)

## 🔐 Authentication Guide

**⚠️ IMPORTANT: This API requires authentication for most endpoints!**

### Default Login Credentials
```
Username: fiap
Password: fiap123
```

### How to Authenticate

#### Method 1: Using Swagger UI (Recommended)
1. Go to http://localhost:8000/docs
2. Click the **"Authorize"** button (🔒) in the top-right corner
3. Enter your credentials:
   - Username: `fiap`
   - Password: `fiap123`
4. Click "Authorize"
5. Now you can test all protected endpoints!

#### Method 2: Using curl/HTTP requests
1. **Login** to get a token:
   ```bash
   curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "fiap", "password": "fiap123"}'
   ```

2. **Use the token** for protected endpoints:
   ```bash
   curl -X POST "http://localhost:8000/predict" \
        -H "Authorization: Bearer <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"city": "vancouver", "state": "BC", "building_type": "highrise", "bedrooms": 2, "bathrooms": 2, "size": 700, "allow_pets": true, "allow_smoking": false, "furnished": false, "count_private_parking": 1, "lease_type": "long_term", "rental_type": "long_term"}'
   ```

## Authentication Details

The API uses JWT (JSON Web Token) based authentication. To access protected endpoints:

1. **Login** - Send a POST request to `/login` with username and password:
   ```json
   {
     "username": "fiap",
     "password": "fiap123"
   }
   ```

2. **Get Token** - The response will include an access token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

3. **Use Token** - Include the token in the Authorization header for protected endpoints:
   ```
   Authorization: Bearer <your_access_token>
   ```

### Default Credentials
- **Username**: `fiap`
- **Password**: `fiap123`

**Note**: The current implementation uses hardcoded credentials for simplicity. In production, implement proper user management with a database.

## Prerequisites

### Option 1: Local Development
- Python 3.8 or higher
- pip (Python package installer)

### Option 2: Docker Deployment
- Docker
- Docker Compose (optional, for easier deployment)

## Installation

### Option 1: Local Development

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd fiap_5mlet_tcm3_grp5
   
   # Or simply download the files to your local directory
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **New Authentication Dependencies:**
   - `python-jose[cryptography]` - JWT token handling
   - `passlib[bcrypt]` - Password hashing
   - `python-dotenv` - Environment variable management

### Option 2: Docker Deployment

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd fiap_5mlet_tcm3_grp5
   
   # Or simply download the files to your local directory
   ```

2. **Build and run with Docker Compose (Recommended)**
   ```bash
   # Build and start the container
   docker-compose up --build
   
   # Or run in detached mode
   docker-compose up --build -d
   ```

3. **Or build and run with Docker directly**
   ```bash
   # Build the Docker image
   docker build -t rental-prediction-api .
   
   # Run the container
   docker run -p 8000:8000 -v $(pwd)/trained_model:/app/trained_model:ro rental-prediction-api
   ```

## Usage

### Starting the API Server

#### Local Development

1. **Make sure your model file is in the correct location**
   ```
   trained_model/
   └── random_forest_rental_price_model.pkl
   ```

2. **Start the server**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Docker Deployment

1. **Make sure your model file is in the correct location**
   ```
   trained_model/
   └── random_forest_rental_price_model.pkl
   ```

2. **Start with Docker Compose (Recommended)**
   ```bash
   # Start the service
   docker-compose up
   
   # Or start in detached mode
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop the service
   docker-compose down
   ```

3. **Or start with Docker directly**
   ```bash
   # Build and run
   docker build -t rental-prediction-api .
   docker run -p 8000:8000 -v $(pwd)/trained_model:/app/trained_model:ro rental-prediction-api
   ```

### Accessing the API

**The API will be available at:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Making Predictions

#### Using the Interactive Documentation

1. Go to http://localhost:8000/docs
2. Click on the `POST /predict` endpoint
3. Click "Try it out"
4. Fill in the request body with your property data
5. Click "Execute"

#### Using curl

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "city": "vancouver",
       "state": "BC",
       "building_type": "highrise",
       "bedrooms": 2,
       "bathrooms": 2,
       "size": 700,
       "allow_pets": true,
       "allow_smoking": false,
       "furnished": false,
       "count_private_parking": 1,
       "lease_type": "long_term",
       "rental_type": "long_term"
     }'
```

#### Using Python requests

```python
import requests

url = "http://localhost:8000/predict"
data = {
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

response = requests.post(url, json=data)
result = response.json()
print(f"Predicted price: ${result['predicted_price']:.2f}")
```

## Input Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `city` | string | City name | "vancouver" |
| `state` | string | State abbreviation | "BC" |
| `building_type` | string | Type of building | "highrise" |
| `bedrooms` | integer | Number of bedrooms (≥0) | 2 |
| `bathrooms` | integer | Number of bathrooms (≥0) | 2 |
| `size` | integer | Property size in square meters (>0) | 700 |
| `allow_pets` | boolean | Whether pets are allowed | true |
| `allow_smoking` | boolean | Whether smoking is allowed | false |
| `furnished` | boolean | Whether property is furnished | false |
| `count_private_parking` | integer | Number of private parking spaces (≥0) | 1 |
| `lease_type` | string | Type of lease | "long_term" |
| `rental_type` | string | Type of rental | "long_term" |

## Response Format

```json
{
  "predicted_price": 2500.50,
  "input_data": {
    "city": "vancouver",
    "state": "BC",
    "building_type": "highrise",
    "bedrooms": 2,
    "bathrooms": 2,
    "size": 700,
    "allow_pets": true,
    "allow_smoking": false,
    "furnished": false,
    "count_private_parking": 1,
    "lease_type": "long_term",
    "rental_type": "long_term"
  }
}
```

## Project Structure

```
fiap_5mlet_tcm3_grp5/
├── __init__.py                      # Package initialization
├── main.py                          # FastAPI application (main entry point)
├── models.py                        # Pydantic data models
├── ml_service.py                    # Machine learning service
├── config.py                        # Configuration settings
├── utils.py                         # Utility functions
├── auth_service.py                  # Authentication service and JWT handling
├── test_api.py                      # API test script
├── start_api.sh                     # Unix/Linux startup script
├── start_api.bat                    # Windows startup script
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── colab_api.py                    # Original Colab code
├── Dockerfile                       # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
├── .dockerignore                   # Docker ignore file
└── trained_model/
    └── random_forest_rental_price_model.pkl  # Trained model
```

### Code Organization

- **`main.py`**: FastAPI application with route handlers and authentication
- **`models.py`**: Pydantic models for request/response validation and authentication
- **`ml_service.py`**: Machine learning logic and model operations
- **`auth_service.py`**: Authentication service with JWT token handling and user management
- **`config.py`**: Configuration settings and constants
- **`utils.py`**: Utility functions (coordinates, formatting, etc.)
- **`test_api.py`**: Comprehensive API testing script
- **`Dockerfile`**: Docker container configuration
- **`docker-compose.yml`**: Docker Compose service definition
- **`.dockerignore`**: Files to exclude from Docker build context

## Testing

### Running the Test Suite

The project includes a comprehensive test script to verify API functionality.

1. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server first** (in one terminal):
   ```bash
   python main.py
   ```

3. **Run the tests** (in another terminal):
   ```bash
   python test_api.py
   ```

### Testing Authentication

You can test the authentication functionality using the Swagger UI at http://localhost:8000/docs or by making HTTP requests:

1. **Login** - POST to `/login` with credentials:
   ```bash
   curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "fiap", "password": "fiap123"}'
   ```

2. **Use the token** - Include the returned token in Authorization header:
   ```bash
   curl -X POST "http://localhost:8000/predict" \
        -H "Authorization: Bearer <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"city": "vancouver", "state": "BC", "building_type": "highrise", "bedrooms": 2, "bathrooms": 2, "size": 700, "allow_pets": true, "allow_smoking": false, "furnished": false, "count_private_parking": 1, "lease_type": "long_term", "rental_type": "long_term"}'
   ```

The test script will:
- ✅ Check if the API server is running
- ✅ Test the health endpoint
- ✅ Test the root endpoint
- ✅ Test the prediction endpoint with valid data
- ✅ Test input validation with invalid data

### Test Output Example

```
Testing Rental Price Prediction API...
==================================================
1. Testing health endpoint...
✅ Health check passed
   Response: {'status': 'healthy', 'model_loaded': True}

2. Testing root endpoint...
✅ Root endpoint passed
   Response: {'message': 'Rental Price Prediction API', 'version': '1.0.0', 'docs': '/docs', 'health': '/health'}

3. Testing prediction endpoint...
✅ Prediction endpoint passed
   Predicted price: $2500.50
   Input data: {
     "city": "vancouver",
     "state": "BC",
     ...
   }

4. Testing invalid input...
✅ Input validation working correctly
   Validation error: {'detail': [{'loc': ['body', 'bedrooms'], 'msg': 'ensure this value is greater than or equal to 0', 'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}

==================================================
Test completed!
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reloading when code changes are detected.

### Testing the API

You can test the API using the built-in Swagger UI at http://localhost:8000/docs or by making HTTP requests using tools like:
- curl
- Postman
- Python requests library
- Any HTTP client

## Troubleshooting

### Common Issues

1. **Authentication Issues**
   - **"Not authenticated" error**: Make sure you're logged in via Swagger UI or using a valid token
   - **"Incorrect username or password"**: Use the exact credentials: username `fiap`, password `fiap123`
   - **Token expired**: Login again to get a new token (tokens expire after 30 minutes)
   - **Can't see Authorize button**: Make sure you're at http://localhost:8000/docs

2. **Model file not found**
   - Ensure `random_forest_rental_price_model.pkl` is in the `trained_model/` directory
   - Check file permissions

3. **Port already in use**
   - Change the port in `main.py` or use a different port with uvicorn
   - Example: `uvicorn main:app --port 8001`
   - For Docker: Change the port mapping in `docker-compose.yml` or use `-p 8001:8000`

4. **Dependencies not installed**
   - Make sure you've activated your virtual environment
   - Run `pip install -r requirements.txt` again

5. **Import errors**
   - Ensure all dependencies are installed correctly
   - Check Python version compatibility (3.8+)

### Docker-Specific Issues

1. **Container fails to start**
   - Check if the model file exists in the `trained_model/` directory
   - Verify Docker is running: `docker --version`
   - Check container logs: `docker-compose logs` or `docker logs <container_name>`

2. **Model not loading in container**
   - Ensure the volume mount is correct in `docker-compose.yml`
   - Check file permissions on the model file
   - Verify the model file path in the container

3. **Port conflicts with Docker**
   - Stop other services using port 8000
   - Use a different port mapping: `-p 8001:8000`
   - Update `docker-compose.yml` to use a different host port

4. **Docker build fails**
   - Check if all required files are present
   - Verify the Dockerfile syntax
   - Try building without cache: `docker build --no-cache -t rental-prediction-api .`

### Health Check

You can check if the API is running properly by visiting:
- http://localhost:8000/health

This will return the API status and whether the model is loaded.

## Future Enhancements

- [ ] Implement coordinate lookup from database
- [ ] Add preprocessing pipeline loading
- [ ] Add model versioning
- [ ] Add logging
- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Add caching for predictions

## License

This project is part of the FIAP 5MLET TCM3 Group 5 assignment.

