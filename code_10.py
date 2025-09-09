from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.model_selection import train_test_split


Student_Performance = pd.read_excel("Student_Performance.xlsx")
X = Student_Performance.iloc[:,:-1]
# Convert 'Yes' to 1 and 'No' to 0 in the specified column
X["Extracurricular Activities"] = X["Extracurricular Activities"].map({"Yes": 1, "No": 0})
y= Student_Performance.iloc[:,-1]

df_cleaned = X.dropna()
y_cleaned = y.loc[df_cleaned.index]  # Keep only corresponding indices in y
X_train_80, X_test_20, y_train_80, y_test_20 = train_test_split(df_cleaned, y_cleaned, test_size=0.2, random_state=42)

model = RandomForestRegressor()
scores = cross_val_score(model, X_train_80, y_train_80, cv=5)  # 5-Fold Cross-Validation
print("Cross-validation scores:", scores)
print("Mean accuracy:", scores.mean())
