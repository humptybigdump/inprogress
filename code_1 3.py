from sklearn.impute import KNNImputer
import numpy as np
import pandas as pd
data = {
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, np.nan, 2.0, None, 5.0],
'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005, 0.02]
}
data = pd.DataFrame(data)
imputer = KNNImputer(n_neighbors=2)
#n_neighbors:Number of neighboring samples to use for imputation.
imputer.fit_transform(data)
