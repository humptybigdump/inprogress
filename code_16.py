import csv

# Writing structured data to a CSV file
data = [
    ["Sample", "Concentration (mg/L)"],
    ["Site A", 2.5],
    ["Site B", 1.8],
    ["Site C", 3.2]
]

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV file written successfully.")
