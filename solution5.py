import math
from typing_extensions import Self, override
#from typing import Self, override

# Define a new class for wells:
class SingleWell:
    def __init__(self, id: str, depth: float, concentration: float, pos: tuple[float, float]):
        self.id = id
        self.depth = depth
        self.concentration = concentration
        self.converted: bool = False
        self.pos = pos

    def is_valid(self) -> bool:
        """
            Returns true if the well concentration is valid.
        """
        return self.concentration > 0.0

    def convert_concentration(self):
        """
            Converts the well concentration from mg/L to g/L.
        """
        if not self.converted:
            self.concentration = self.concentration / 1000.0
            self.converted = True
            print('Converting process done') 
        else:
            print('It has been already converted')    

    def calculate_distance(self, other: Self) -> float:
        """
            Calculates the distance between two wells.
        """
        dx: float = self.pos[0] - other.pos[0]
        dy: float = self.pos[1] - other.pos[1]

        return math.hypot(dx, dy)

# Additional (not in the exercise):
class RestrictedWell(SingleWell):
    def __init__(self, id: str, depth: float, concentration: float, pos: tuple[float, float]):
        super().__init__(id, depth, concentration, pos)

    @override
    def is_valid(self) -> bool:
        if self.converted:
            return self.concentration > (1.1 / 1000.0)
        else:
            return self.concentration > 1.1

# Define a class for all wells:
class WellContainer:
    def __init__(self):
        self.wells = []

    def add_well(self, well: SingleWell):
        """
            Adds a new well to the container.
            The id must be unique!
        """
        for w in self.wells:
            if w.id == well.id:
                raise ValueError(f"Well already in container: {w.id}")

        self.wells.append(well)

    def add_multiple_wells(self, wells: list):
        for w in wells:
            self.add_well(w)

    def all_valid_wells(self):
        """
            Returns a generator with all the valid wells.
        """
        return (w for w in self.wells if w.is_valid())

    def all_invalid_wells(self):
        """
            Returns a generator with all the invalid wells.
        """
        return (w for w in self.wells if not w.is_valid())

    def fix_all_concentrations(self):
        """
            Fixes the concentration for all the invalid wells.
            Uses the mean value to fill in the invalid values.
        """
        valid_values: list[float] = [w.concentration for w in self.all_valid_wells()]
        mean: float = sum(valid_values) / float(len(valid_values))

        for w in self.all_invalid_wells():
            w.concentration = mean

    def convert_concentration(self):
        for w in self.all_valid_wells():
            w.convert_concentration()

    def all_distances(self) -> list[tuple[float, str, str]]:
        """
            Calculates all the distances between all the wells.
            Returns a list with sorted distances and well ids.
        """
        result: list[tuple[float, str, str]] = []

        for w1 in self.all_valid_wells():
            for w2 in self.all_valid_wells():
                if w1.id != w2.id:
                    d: float = w1.calculate_distance(w2)
                    result.append((d, w1.id, w2.id))

        return sorted(result, key=lambda vals: vals[0])

def main():
    # Create an empty well container
    wc = WellContainer()

    # Add some wells to test the code:
    wc.add_well(SingleWell("A1", 10.0, 5.0, (12.2, 5.7)))
    wc.add_well(SingleWell("A2", 15.0, 0.0, (2.9, 7.0)))
    wc.add_well(SingleWell("A3", 20.0, 8.0, (15.3, 1.9)))
    wc.add_well(SingleWell("A4", 25.0, 3.0, (9.6, 8.2)))
    wc.add_well(SingleWell("A5", 30.0, 0.0, (1.5, 7.3)))

    # Do some calculations.
    wc.fix_all_concentrations()
    wc.convert_concentration()
    # Try to convert two times:
    wc.convert_concentration()
    distances = wc.all_distances()

    # Print the results:
    print(f"Shortest distance: {distances[0]}")
    print(f"Longest distance: {distances[-1]}")

    for w in wc.wells:
        print(f"{w.id}: {w.concentration}")

    print("\n\n")

    # Additional (not in exercise):
    b1 = RestrictedWell("B1", 11.0, 0.5, (12.2, 19.7))
    b2 = RestrictedWell("B2", 9.5, 8.3, (5.7, 6.2))

    wc.add_multiple_wells([b1, b2])

    wc.fix_all_concentrations()
    wc.convert_concentration()

    distances = wc.all_distances()

    print(f"Shortest distance: {distances[0]}")
    print(f"Longest distance: {distances[-1]}")

    for w in wc.wells:
        print(f"{w.id}: {w.concentration}")

if __name__ == "__main__":
    main()

