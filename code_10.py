pattern = r"water"
text = "The water level is rising."
match = re.search(pattern, text)
if match:
    print("Pattern found:", match.group())
else:
    print("Pattern not found.")
