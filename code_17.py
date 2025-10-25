# Creating a DataFrame
data = {
    "Sample": ["Site A", "Site B", "Site C"],
    "Concentration (mg/L)": [2.5, 1.8, 3.2]
}

df = pd.DataFrame(data)

# Writing to an Excel file
df.to_excel("output.xlsx", index=False)

print("Excel file written successfully.")
