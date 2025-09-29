import joblib
import pandas as pd
import numpy as np

# Define the path to the saved model
model_load_path = 'train/random_forest_rental_price_model.pkl'

# Load the model
loaded_model = joblib.load(model_load_path)

print("Modelo carregado com sucesso!")

# Example of a new data sample (replace with your actual data)
# This should be a pandas DataFrame with the same columns as the original data before preprocessing
new_data_sample = pd.DataFrame({
    'longitude': [-79.416300],
    'latitude': [43.700110],
    'neighborhood': ['unknown'],  # Use 'unknown' if neighborhood is missing or not in training
    'city': ['sao paulo'],
    'state': ['BC'],
    'building_type_txt_id': ['highrise'],
    'student_friendly': [0],
    'building_amenity': [np.nan], # Use np.nan for missing values
    'total_rooms': [2.0],
    'total_bathrooms': [2.0],
    'size': [700.0],
    'verified_state_machine': ['approved'], # Use 'approved' if state machine is not in training
    'allow_pets': [1],
    'allow_smoking': [0.0],
    'furnished': [0.0],
    'count_private_parking': [1.0],
    'lease_type': ['long_term'],
    'rental_type': ['long_term'],
    'listing_utility': [np.nan], # Use np.nan for missing values
    'price_frequency': ['monthly'],
    'price_monthly': [0.0] # This column is not used for prediction, can be any value
})

# Ensure the columns match the original training data before preprocessing
# This step is crucial to avoid errors during transformation
# You might need to adjust the column order or add/remove columns if your original data had more
# or fewer columns than this example.
original_training_columns = stratified_training_dataset.drop("price", axis=1).columns
new_data_sample = new_data_sample.reindex(columns=original_training_columns, fill_value=np.nan)


# Preprocess the new data sample using the same pipeline fitted on the training data
# The 'full_pipeline' variable is still in the environment from previous steps
new_data_sample_prepared = full_pipeline.transform(new_data_sample)

# Make a prediction
predicted_price = loaded_model.predict(new_data_sample_prepared)

print(f"Predicted price for the new sample: {predicted_price[0]:.2f}")