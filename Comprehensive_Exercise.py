# General packages
import pandas as pd
from pathlib import Path



#Visualization
import seaborn as sns
import matplotlib.pyplot as plt


# Task 1: Load and Inspect the Dataset
# ----------------------------------------
# Load dataset from CSV file
script_path = Path(__file__).resolve()
script_dir = script_path.parent
file_path = script_dir / "all_data_multiple.csv"
df = pd.read_csv(file_path)
df=df.loc[1:,:]
# Convert 'Timestamp' column to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Display dataset information
print(df.info())
print(df.head())

# Task 2: Handle Missing Values
# ----------------------------------------
# Identify missing values
print("Missing Values Before Handling:\n", df.isnull().sum())

# Option 1: Drop rows where all values are missing
df_dropped = df.dropna()

# Option 2: Impute missing values with column mean
df.iloc[:, 2:] = df.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')

# Impute missing values with column mean
df_imputed = df.fillna(df.iloc[:, 2:].mean())

# Print missing values after handling
print("Missing values after dropping:", df_dropped.isna().sum().sum())
print("Missing values after imputation:", df_imputed.isna().sum().sum())

# Task 3: Extract Temporal Features
# ----------------------------------------
# Set Timestamp as index
df=df_imputed
df.set_index("Timestamp", inplace=True)

# Extract year, month, and hour
df["year"] = df.index.year
df["month"] = df.index.month
df["hour"] = df.index.hour

print(df[["year", "month", "hour"]].head())  # Display extracted time features

# Task 4: Visualize Weather Data
# ----------------------------------------
# A. Time-Series Plot for Air Temperature
plt.figure(figsize=(14, 6))
plt.plot(df.index, df["Precipitation"], color="red", alpha=0.8)
plt.xlabel("Date")
plt.ylabel("Precipitation (mm)")
plt.title("Task4.1:Precipitation Over Time")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# B. Violin Plot for Air Temperature by Year
plt.figure(figsize=(12, 6))
sns.violinplot(x="year", y="Air temperature", data=df, palette="viridis")
plt.xlabel("Year")
plt.ylabel("Air Temperature (°C)")
plt.title("Task4.2A:Violin Plot of Air Temperature by Year")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()


# Filter the dataframe to include only temperatures greater than 0°C
df_filtered = df[df["Air temperature"] > 0]

# Violin Plot for Air Temperature by Year (filtered for temperatures > 0)
plt.figure(figsize=(12, 6))
sns.violinplot(x="year", y="Air temperature", data=df_filtered, palette="viridis")

# Labels and formatting
plt.xlabel("Year")
plt.ylabel("Air Temperature (°C)")
plt.title("Task4.2B: Violin Plot of Air Temperature by Year (T > 0°C)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)

# Show the plot
plt.show()


# C. Box Plot for Wind Speed by Month
plt.figure(figsize=(12, 6))
sns.boxplot(x="month", y="Wind speed", data=df, palette="coolwarm")
plt.xlabel("Month")
plt.ylabel("Wind Speed (m/s)")
plt.title("Task4.3:Wind Speed Distribution by Month")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# Task 5: Aggregate Data
# ----------------------------------------
# A. Daily Average Air Temperature
df_daily_avg = df["Air temperature"].resample("D").mean()
plt.figure(figsize=(14, 6))
plt.plot(df_daily_avg.index, df_daily_avg, color="orange", linestyle="-", marker="o")
plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.title("Daily Average Temperature")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()

# B. Monthly Mean Humidity
df_monthly_avg = df["Air relative humidity"].resample("M").mean()
plt.figure(figsize=(14, 6))
plt.plot(df_monthly_avg.index, df_monthly_avg, color="green", linestyle="-", marker="s")
plt.xlabel("Date")
plt.ylabel("Mean Relative Humidity (%)")
plt.title("Monthly Mean Humidity")
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
