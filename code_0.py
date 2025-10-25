import random 
random.seed(42)

class Soil:
    """Represents a soil sample with sand, silt, and clay composition."""
    
    def __init__(self):
        self.sand, self.silt, self.clay = self.generate_soil_composition()
        self.category = self.categorize_soil()
    
    def generate_soil_composition(self):
        """Generates random sand, silt, and clay content summing to 100%."""
        sand = random.uniform(0, 100)
        silt = random.uniform(0, 100 - sand)
        clay = 100 - sand - silt
        return round(sand, 1), round(silt, 1), round(clay, 1)
    
    def categorize_soil(self):
        """Categorizes soil based on the sand, silt, and clay composition."""
        if self.sand > 70:
            return "Sandy Soil"
        elif self.clay > 40:
            return "Clay Soil"
        elif self.silt > 40:
            return "Silty Soil"
        elif self.sand > 50 and self.silt > 20:
            return "Loamy Sand"
        elif self.silt > 50 and self.clay > 20:
            return "Silty Clay"
        else:
            return "Loam"

    def describe(self):
        """Returns a formatted description of the soil composition and category."""
        return (f"Soil Composition: Sand = {self.sand}%, Silt = {self.silt}%, Clay = {self.clay}%\n"
                f"Classified as: {self.category}")

# Example Usage: Generate and classify 2 soil samples
for _ in range(2):
    soil_sample = Soil()
    print(soil_sample.describe())
