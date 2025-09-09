from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
data = {
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, np.nan, 2.0, None, 5.0],
'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005, 0.02]
}
data = pd.DataFrame(data)

X = data.iloc[:,:-1]
y = data.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

