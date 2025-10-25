from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
data = {
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, np.nan, 2.0, None, 5.0],
'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005, 0.02]
}
data = pd.DataFrame(data)
# Initialize the scaler
scaler = MinMaxScaler()

# Fit the scaler to the data before transforming
scaler.fit(data)  # Learn the mean and standard deviation

# Now transform the data
scaled_data = scaler.transform(data)
print(np.std(pd.DataFrame(scaled_data)[0]))
print(np.mean(pd.DataFrame(scaled_data)[0]))
