#!/usr/bin/env python3
"""
Simple test script for the Rental Price Prediction API
"""

try:
    import requests
    import json
    import time
except ImportError as e:
    print("❌ Missing required dependency:", str(e))
    print("\nTo fix this, install the required dependencies:")
    print("pip install -r requirements.txt")
    print("\nOr install requests directly:")
    print("pip install requests")
    exit(1)

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Rental Price Prediction API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
        return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    print()
    
    # Test 2: Root endpoint
    print("2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    print()
    
    # Test 3: Prediction endpoint
    print("3. Testing prediction endpoint...")
    test_data = {
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
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction endpoint passed")
            print(f"   Predicted price: ${result['predicted_price']:.2f}")
            print(f"   Input data: {json.dumps(result['input_data'], indent=2)}")
        else:
            print(f"❌ Prediction endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Prediction endpoint error: {e}")
    
    print()
    
    # Test 4: Invalid input
    print("4. Testing invalid input...")
    invalid_data = {
        "city": "vancouver",
        "state": "BC",
        "building_type": "highrise",
        "bedrooms": -1,  # Invalid: negative bedrooms
        "bathrooms": 2,
        "size": 700,
        "allow_pets": True,
        "allow_smoking": False,
        "furnished": False,
        "count_private_parking": 1,
        "lease_type": "long_term",
        "rental_type": "long_term"
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:  # Validation error
            print("✅ Input validation working correctly")
            print(f"   Validation error: {response.json()}")
        else:
            print(f"❌ Input validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Input validation test error: {e}")
    
    print()
    print("=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_api()

