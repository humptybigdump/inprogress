pattern = r"\d+"  # Matches one or more digits
text = "There are 12 wells, 5 monitoring stations, and 100 samples."
matches = re.findall(pattern, text)
print("Matches found:", matches)
