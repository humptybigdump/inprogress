# main.py
import soil_data_generator
import soil_acidic
import numpy as np
# Generate synthetic soil data
num_samples = 100  # Generate 100 samples
df = soil_data_generator.generate_soil_data(num_samples)

# Clean the generated data
df_cleaned = soil_acidic.filter_acidic_soils(df)

# Display the cleaned data
print("Cleaned Soil Sample Data:")
print(df_cleaned.head())
print(np.shape(df_cleaned))

