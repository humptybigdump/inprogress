import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
data = {
'WellID': [101, 102, 103, 104, 105],
'Nitrate_mg_L': [3.5, np.nan, 2.0, None, 5.0],
'Arsenic_mg_L': [0.01, 0.03, np.nan, 0.005, 0.02]
}
data = pd.DataFrame(data)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
#imputer = SimpleImputer(missing_values="whatever values you consider as missing values for example:" -1, strategy='mean')
#or strategy='median'
pd.DataFrame(imputer.fit_transform(data))
