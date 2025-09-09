import numpy as np
import random
import pandas as pd

np.random.seed(42)
# Task1: Generate sorbed concentration (Cs) - Uniform distribution [mg/kg]
Cs = np.random.uniform(low=1, high=20, size=365)
# Generate aqueous concentration (Cw) - Normal distribution [mg/L]
Cw = np.random.normal(loc=1, scale=0.5, size=365)
Cw[Cw <= 0] = 0.1  # Ensure no negative or zero values
#Task2: Calculate distribution coefficient (Kd) [L/kg]
Kd = Cs / Cw
#Task3: Generate bulk density (ρ_b) [g/cm$^3$] - Normal distribution
bulk_density = np.random.normal(loc=1.6, scale=0.2, size=365)
bulk_density = np.clip(bulk_density, 1.2, 2.0)  # Limit realistic range
# Generate porosity (theta) - Uniform distribution
porosity = np.random.uniform(low=0.2, high=0.5, size=365)
#Task4: Calculate retardation factor (Rf)
Rf = 1 + (bulk_density * Kd) / porosity
# Compile into DataFrame
df = pd.DataFrame({
    "Cs_mg_kg": Cs,"Cw_mg_L": Cw,"Kd_L_kg": Kd, "BulkDensity_g_cm3": bulk_density,"Porosity": porosity,"RetardationFactor": Rf
})
print("Generated Data:\n", df.head())
#Task5: Apply Filtering ---
filtered_df = pd.DataFrame([high_r for high_r in df['RetardationFactor'] if high_r > 50])
print("\nFiltered Data (Rf > 50):\n", filtered_df.head())
#Task6: Clean and Handle Missing Values ---
for _ in range(int(len(df) * 0.05)):
    idx = random.randint(0, len(df) - 1)
    col = random.choice(['Kd_L_kg', 'RetardationFactor'])
    df.at[idx, col] = np.nan
print("\nMissing Values:\n", df.isnull().sum())
# Fill missing values with column means
df['Kd_L_kg'].fillna(df['Kd_L_kg'].mean(), inplace=True)
df['RetardationFactor'].fillna(df['RetardationFactor'].mean(), inplace=True)
#Task7: Remove duplicates if any
df = df.drop_duplicates()
print("\nData after cleaning:\n", df.head())