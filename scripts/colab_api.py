import joblib
import pandas as pd
import numpy as np

# Define the path to the saved model
model_load_path = 'trained_model/random_forest_rental_price_model_v1_31.pkl'

# Load the model
loaded_model = joblib.load(model_load_path)

print("Modelo carregado com sucesso!")

# Example of a new data sample (replace with your actual data)
# This should be a pandas DataFrame with the same columns as the original data before preprocessing
new_data_sample = pd.DataFrame({
    'longitude': [-79.416300],
    'latitude': [43.700110],
    'neighborhood': ['unknown'],  # Use 'unknown' if neighborhood is missing or not in training
    'city': ['vancouver'],
    'state': ['BC'],
    'building_type_txt_id': ['highrise'],
    'student_friendly': [0],
    'building_amenity': [None],
    'total_rooms': [2.0],
    'total_bathrooms': [2.0],
    'size': [700.0],
    'verified_state_machine': ['approved'],
    'allow_pets': [1],
    'allow_smoking': [0.0],
    'furnished': [0.0],
    'count_private_parking': [0.0],
    'lease_type': ['long_term'],
    'rental_type': ['long_term'],
    'listing_utility': [None],
    'price_frequency': ['monthly'],
    'price_monthly': [0.0] # This column is not used for prediction, can be any value
})

# Note: This script assumes you have the preprocessing pipeline available
# In a real scenario, you would need to load the preprocessing pipeline as well
# For now, we'll create a simple preprocessing approach

# Handle categorical variables with one-hot encoding
categorical_columns = ['neighborhood', 'city', 'state', 'building_type_txt_id', 
                      'verified_state_machine', 'lease_type', 'rental_type', 'price_frequency']

processed_data = new_data_sample.copy()

for col in categorical_columns:
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

# Adjust feature count to match expected features (165 features)
expected_features = 165
current_features = processed_data.shape[1]

if current_features < expected_features:
    # Add zero columns to match expected feature count
    missing_features = expected_features - current_features
    zero_columns = pd.DataFrame(
        np.zeros((processed_data.shape[0], missing_features)),
        columns=[f'feature_{i}' for i in range(missing_features)],
        index=processed_data.index
    )
    processed_data = pd.concat([processed_data, zero_columns], axis=1)
elif current_features > expected_features:
    # Truncate if we have too many features
    processed_data = processed_data.iloc[:, :expected_features]

new_data_sample_prepared = processed_data

# Make a prediction
predicted_price = loaded_model.predict(new_data_sample_prepared)

print(f"Predicted price for the new sample: {predicted_price[0]:.2f}")