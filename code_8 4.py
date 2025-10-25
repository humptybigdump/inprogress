from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

data = {
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, np.nan, 2.0, None, 5.0],
'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005, 0.02]
}
data = pd.DataFrame(data)
imputer = KNNImputer(n_neighbors=2)
#n_neighbors:Number of neighboring samples to use for imputation.
data = pd.DataFrame(imputer.fit_transform(data))
X = data.iloc[:,:-1]
y = data.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)  # Training the model
print(model)