import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Example observed and predicted values
y_true = np.array([3, -0.5, 2, 7])
y_pred = np.array([2.5, 0.0, 2, 8])

# Compute MAE, MSE, RMSE
mae = mean_absolute_error(y_true, y_pred)
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_true, y_pred)


# Compute NRMSE and RRMSE (using normalization)
nrmse = rmse / (max(y_true)-min(y_true))
rrmse = rmse / np.mean(y_true)

# Compute RPD (standard deviation of observed values)
rpd = np.std(y_true) / rmse

print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R^2:", r2)
print("NRMSE:", nrmse)
print("RRMSE:", rrmse)
print("RPD:", rpd)
