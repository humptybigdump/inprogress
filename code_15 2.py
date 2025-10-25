pattern = r"water"
text = "Water samples were collected.\nWater level is high."
matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
print("Matches found:", matches)
