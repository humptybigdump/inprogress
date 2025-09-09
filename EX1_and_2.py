import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt


# ----------------------------------------------
# Task 1: Load Student_Performance.xlsx
# ----------------------------------------------
# Load the Student_Performance.xlsx
# Get the directory of the script file, even when run from elsewhere
script_path = Path(__file__).resolve()
script_dir = script_path.parent


# Build full file path in a platform-independent way
file_path = script_dir / "Student_Performance.xlsx"
Student_Performance = pd.read_excel(file_path)
X = Student_Performance.iloc[:,:-1]
# Convert 'Yes' to 1 and 'No' to 0 in the specified column
X["Extracurricular Activities"] = X["Extracurricular Activities"].map({"Yes": 1, "No": 0})
y= Student_Performance.iloc[:,-1]

# Display original dataset
print("Original Dataset:\n", X.head())


# ----------------------------------------------
# Task 2: Impute Missing Values
# ----------------------------------------------
# Mean Imputation
mean_imputer = SimpleImputer(strategy="mean")
df_mean = pd.DataFrame(mean_imputer.fit_transform(X), columns=X.columns)

# Median Imputation
median_imputer = SimpleImputer(strategy="median")
df_median = pd.DataFrame(median_imputer.fit_transform(X), columns=X.columns)

# KNN Imputation (using 3 nearest neighbors)
knn_imputer = KNNImputer(n_neighbors=3)
df_knn = pd.DataFrame(knn_imputer.fit_transform(X), columns=X.columns)

# Remove rows with remaining missing values
df_cleaned = X.dropna()
y_cleaned = y.loc[df_cleaned.index]  # Keep only corresponding indices in y

# Displaying Statistical Summaries
print("\nStatistical Summary Before Imputation:\n", X.describe())
print("\nStatistical Summary After Mean Imputation:\n", df_mean.describe())
print("\nStatistical Summary After Median Imputation:\n", df_median.describe())
print("\nStatistical Summary After KNN Imputation:\n", df_knn.describe())
print("\nStatistical Summary After Removing Rows with Missing Values:\n", df_cleaned.describe())

# ----------------------------------------------
# Task 3: Feature Scaling (Min-Max and Normalization)
# ----------------------------------------------
scaler_minmax = MinMaxScaler()  # Min-Max Scaling
df_scaled_minmax = pd.DataFrame(scaler_minmax.fit_transform(df_knn), columns=X.columns)

scaler_normal = StandardScaler()  # Normalization
df_scaled_normal = pd.DataFrame(scaler_normal.fit_transform(df_knn), columns=X.columns)

print("\nScaled Dataset (Min-Max Normalization):\n", df_scaled_minmax.head())

# ----------------------------------------------
# Task 4: Splitting Data (80-20 and 70-30)
# ----------------------------------------------
# 80-20 split
X_train_80, X_test_20, y_train_80, y_test_20 = train_test_split(df_scaled_minmax, y, test_size=0.2, random_state=42)

# 70-30 split
X_train_70, X_test_30, y_train_70, y_test_30 = train_test_split(df_scaled_minmax, y, test_size=0.3, random_state=42)

# Display number of samples
print("\nDataset Splitting:")
print(f"80-20 Split: Training Samples = {X_train_80.shape[0]}, Testing Samples = {X_test_20.shape[0]}")
print(f"70-30 Split: Training Samples = {X_train_70.shape[0]}, Testing Samples = {X_test_30.shape[0]}")




# ----------------------------------------------
# Task 1: Train a Linear Regression Model
# ----------------------------------------------

# Initialize and train the model
model = LinearRegression()
# model = LinearRegression()
model.fit(X_train_80, y_train_80)


# ----------------------------------------------
# Task 2: Apply Cross-Validation
# ----------------------------------------------
# Perform 5-Fold Cross-Validation
cv_scores = cross_val_score(model, df_scaled_minmax, y, cv=5, scoring='r2')

print(f"Cross-Validation R² Scores: {cv_scores}")
print(f"Mean R² Score: {np.mean(cv_scores):.4f}")

# ----------------------------------------------
# Task 3: Apply Model Performance Metrics
# ----------------------------------------------

# Predictions on test data
y_pred = model.predict(X_test_20)

# Compute error metrics
mse = mean_squared_error(y_test_20, y_pred)
mae = mean_absolute_error(y_test_20, y_pred)
r2 = r2_score(y_test_20, y_pred)

print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R-squared Score (R²): {r2:.4f}")

# ----------------------------------------------
# Task 4: Model Performance Visualization
# ----------------------------------------------
# Scatter plot of actual vs. predicted values
plt.figure(figsize=(8, 5))
plt.scatter(y_test_20, y_pred, color='blue', alpha=0.6, label="Predicted vs. Actual")
plt.plot([y_test_20.min(), y_test_20.max()], [y_test_20.min(), y_test_20.max()], 'r--', lw=2, label="Ideal Fit")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values in Linear Regression")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()