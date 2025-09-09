# soil_data_generator.py
import numpy as np
import pandas as pd

def generate_soil_data(num_samples):
    """Generate synthetic soil sample data."""
    np.random.seed(0)  # For reproducibility

    # Randomly generate soil properties
    pH = np.random.uniform(4.0, 8.0, num_samples)  # pH values between 4 and 8
    moisture_content = np.random.uniform(10, 50, num_samples)  # Moisture content between 10% and 50%
    nitrogen = np.random.uniform(5, 30, num_samples)  # Nitrogen in mg/kg
    phosphorus = np.random.uniform(2, 15, num_samples)  # Phosphorus in mg/kg
    potassium = np.random.uniform(10, 80, num_samples)  # Potassium in mg/kg

    # Create a DataFrame
    df = pd.DataFrame({
        'pH': pH,
        'Moisture_Content': moisture_content,
        'Nitrogen': nitrogen,
        'Phosphorus': phosphorus,
        'Potassium': potassium
    })
    return df

