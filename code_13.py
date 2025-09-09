pattern = r"well"
replacement = "station"
text = "There are three wells in the area."
new_text = re.sub(pattern, replacement, text)
print("Replaced text:", new_text)
