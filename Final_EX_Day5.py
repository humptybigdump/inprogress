import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor,StackingRegressor
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from sklearn.linear_model import Ridge
from scipy.stats import uniform, randint
import seaborn as sns
from pathlib import Path

script_path = Path(__file__).resolve()
script_dir = script_path.parent


# Load and process PFAS dataset
pfas_path = script_dir / "PFAS_sorption.xlsx"
pfas_xlsx = pd.ExcelFile(pfas_path)
pfas_sheet = "data"
pfas_data = pd.read_excel(pfas_xlsx, sheet_name=pfas_sheet)

# Display dataset information
print("Dataset Information:")
pfas_data.info()

# Check for missing values
print("\nMissing Values:")
print(pfas_data.isnull().sum())

# Display summary statistics
print("\nSummary Statistics:")
print(pfas_data.describe())

# Load and process soil dataset

soil_path = script_dir / "soildata.xlsx"
soil_xlsx = pd.ExcelFile(soil_path)
soil_sheet = "Sheet1"
soil_database = pd.read_excel(soil_xlsx, sheet_name=soil_sheet)
soil_database_processed = soil_database.iloc[:, 6:].reset_index(drop=True)

# Train the KNN imputer
imputer = KNNImputer(n_neighbors=6)
imputer.fit(soil_database_processed)

# Select specific columns for imputation
selected_columns = ["pH", "CEC", "Sand", "Silt", "Clay", "Corg"]
soil_pfas_data = pfas_data[selected_columns]

# Apply imputation
soil_pfas_data_imputed = pd.DataFrame(imputer.transform(soil_pfas_data), columns=soil_pfas_data.columns)

# Update the original dataset with imputed values
pfas_data_imputed = pfas_data.copy()
for col in selected_columns:
    pfas_data_imputed[col] = soil_pfas_data_imputed[col]

# Display summary statistics of the updated dataset
print("\nSummary Statistics of Selected Columns:")
print(pfas_data_imputed[selected_columns].describe())

lats = soil_database['Latitude']
lons = soil_database['Longitude']

# Create a figure and add a geographical projection
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add detailed features to the map (coastlines, countries, rivers, etc.)
ax.coastlines(resolution='10m', linewidth=1)
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)
ax.add_feature(cfeature.LAND, facecolor='#f0e4c8')  # Light earth tone for land
ax.add_feature(cfeature.OCEAN, facecolor='#a4c8ed')  # Light blue for oceans
ax.add_feature(cfeature.LAKES, facecolor='#b0e0e6', edgecolor='black')

# Customizing gridlines
gridlines = ax.gridlines(draw_labels=True, color='gray', alpha=0.7, linestyle='--', linewidth=0.5)

# Scatter plot for the points with more professional styling
scatter = ax.scatter(
    lons, lats, color='darkred', marker='o', s=10, alpha=0.2, 
    transform=ccrs.PlateCarree(), zorder=5
)

# Add a title with a professional style
plt.title("Global Soil Properties Map (SoilGrids Data)", fontsize=16, fontweight='bold', pad=20)

# Show the plot
plt.show()

# Initialize the scaler
scaler = MinMaxScaler()

# Fit the scaler to the data before transforming
scaler.fit(pfas_data_imputed.iloc[:,:-1])  # Learn the mean and standard deviation

# Now transform the data
scaled_data = pd.DataFrame(scaler.transform(pfas_data_imputed.iloc[:,:-1]),columns=pfas_data_imputed.iloc[:,:-1].columns)

X_train, X_test, y_train, y_test = train_test_split(scaled_data, pfas_data_imputed.iloc[:,-1], test_size=0.2, random_state=42)

ridge_params = {"alpha": uniform(0.1, 10)}
rf_params = {
    "n_estimators": randint(50, 200),
    "max_depth": randint(3, 20),
    "min_samples_split": randint(2, 10),
    "min_samples_leaf": randint(1, 10)
}

ridge_search = RandomizedSearchCV(Ridge(), ridge_params, n_iter=20, cv=5, scoring='neg_mean_squared_error', random_state=42)
ridge_search.fit(X_train, y_train)
optimized_ridge = ridge_search.best_estimator_

rf_search = RandomizedSearchCV(RandomForestRegressor(), rf_params, n_iter=20, cv=5, scoring='neg_mean_squared_error', random_state=42)
rf_search.fit(X_train, y_train)
optimized_rf = rf_search.best_estimator_

models = {
    'Linear': LinearRegression(),
    'Ridge': optimized_ridge,
    'RF': optimized_rf,
    'Stacking': StackingRegressor(
        estimators=[('linear', LinearRegression()), ('ridge', optimized_ridge), ('rf', optimized_rf)],
        final_estimator=RandomForestRegressor()
    )
}

def evaluate(model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    residuals = y_test - y_pred
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    metrics = {
        'NRMSE': rmse / (y_test.max() - y_test.min()),
        'RRMSE': rmse / np.mean(y_test),
        'R2': r2_score(y_test, y_pred),
        'CV_NRMSE': np.mean(
            np.sqrt(-cross_val_score(model, X_train, y_train, scoring='neg_mean_squared_error', cv=5)) / (y_train.max() - y_train.min())
        )
    }
    
    # Fancy visualization with residual histogram
    plt.figure(figsize=(8,6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.7, edgecolor=None)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.title(f"Model: {type(model).__name__}")
    
    # Residual histogram as inset
    ax_resid = plt.gca().inset_axes([0.7, 0.1, 0.3, 0.3])
    sns.histplot(residuals, bins=15, kde=True, ax=ax_resid)
    ax_resid.set_title("Residuals")
    ax_resid.set_xticks([])
    ax_resid.set_yticks([])
    
    plt.show()
    
    return metrics

for model in models.values():
    print(evaluate(model))

