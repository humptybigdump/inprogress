import matplotlib.pyplot as plt

# Create a simple plot
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Example Plot")

# Save the figure in different formats
plt.savefig("figure.png")   # Save as PNG
plt.savefig("figure.pdf")   # Save as PDF
plt.savefig("figure.svg")   # Save as SVG
plt.savefig("figure.jpg", dpi=300)  # Save as high-resolution JPEG

# Display the plot
plt.show()
