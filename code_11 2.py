pattern = r"^water"
text = "water samples were collected."
match = re.match(pattern, text)
if match:
    print("Pattern found at the beginning:", match.group())
else:
    print("Pattern not found at the beginning.")
