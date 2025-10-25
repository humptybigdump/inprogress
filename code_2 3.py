# Compute skewness and kurtosis
skewness_value = df["Magnitude"].skew()
kurtosis_value = df["Magnitude"].kurt()
print(f'Skewness: {skewness_value:.2f}, Kurtosis: {kurtosis_value:.2f}')
