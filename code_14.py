# Writing to a text file
with open("example.txt", "w") as file:
    file.write("This is a sample text file.\n")
    file.write("Python makes file handling easy.")

print("File written successfully.")
