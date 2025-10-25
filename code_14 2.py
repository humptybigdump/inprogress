pattern = r"(\d{3})-(\d{2})-(\d{4})"  # Social Security Number pattern
text = "The well identifier is 123-45-6789."
match = re.search(pattern, text)
if match:
    print("Full match:", match.group(0))
    print("Area code:", match.group(1))
    print("Group:", match.group(2))
    print("Serial:", match.group(3))
else:
    print("Pattern not found.")
