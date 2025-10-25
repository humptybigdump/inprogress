# Assignment 05 - AdvancedBILS
# to run the script: python A05.py "path to csv file"

import sys
import pandas as pd
import matplotlib.pyplot as plt

# Task 3
# a)
# Load the dataset. Read the file into a DataFrame and display the first 5 rows
inputfile = sys.argv[1]
df = pd.read_csv(inputfile)

print(df.head())

# b)
# Create a new DataFrame that counts how many detections occurred at each position across all patients.
detections_per_pos = df[df["Detection"] == 1].groupby("Position").size().reset_index(name="Detection_Count")
print(detections_per_pos.head())

# c)
# Create a bar plot showing the number of detections at each position (x-axis: Position, y-axis: Count of
# Detections). Add a title and axis labels.
detections_per_pos['Detection_Count'].plot(kind='bar',
                                           title='Detections per Position',
                                           xlabel='Position',
                                           ylabel='Count of Detections',
                                           xticks=range(len(detections_per_pos))[::25])
plt.savefig('detections_per_position.png')  # save plot as file (can be png or pdf)
# plt.show()  # show plot in interactive window


# d)
# Assuming detections are false positives that follow a Poisson distribution with λ= 0.5, identify all
# positions where the number of detections is 7 or more. Print those positions and their counts.
threshold = 7
potential_epitopes = detections_per_pos[detections_per_pos["Detection_Count"] >= threshold]
print(f"\nPositions with {threshold} or more detections (Potential epitopes):")
print(potential_epitopes)

# e)
#  Save the filtered list of potential epitopes (from task d) into a new CSV file called potential_epitopes.csv.
potential_epitopes.to_csv("potential_epitopes.csv", index=False)

# f)
# Use .describe() to compute summary statistics of the detection counts per position. Then write one or
# two sentences in a print statement summarizing whether the detections seem evenly distributed or whether
# some positions stand out.
summary_stats = detections_per_pos["Detection_Count"].describe()
print("\nSummary statistics of detection counts per position:")
print(summary_stats)

# Interpretation might be:
print("\nInterpretation:")
if summary_stats["max"] > summary_stats["mean"] + 2 * summary_stats["std"]:
    print("Some positions have unusually high detection counts (mean + 2*std), suggesting they may be true epitopes rather than random noise.")
else:
    print("The detection counts appear fairly evenly distributed, suggesting mostly random false positives.")