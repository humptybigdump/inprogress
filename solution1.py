from typing import override

class PFASCompound:
    """Base class representing a PFAS compound."""

    def __init__(self, name, cf2_count):
        """
        Initializes a PFAS compound with its name and CF2 chain length.
        :param name: The chemical name of the PFAS.
        :param cf2_count: Number of CF2 groups in the PFAS structure.
        """
        self.name = name  # Name of the PFAS compound
        self.cf2_count = cf2_count  # Number of CF2 groups (used for classification)

    def describe(self):
        """
        Provides a general description of the PFAS compound.
        """
        return f"{self.name}: CF2 Chain Length = {self.cf2_count}"

    def environmental_impact(self) -> str:
        raise RuntimeError("You have to implement the method 'environmental_impact'")


class LongChainPFAS(PFASCompound):
    """Subclass representing long-chain PFAS (CF2 count > 7)."""

    def __init__(self, name, cf2_count):
        super().__init__(name, cf2_count)
        self.solubility = "Low"
        self.bioaccumulation_potential = "High"

    @override
    def environmental_impact(self) -> str:
        """Describes the environmental impact of long-chain PFAS."""
        return (f"{self.name} (Long-Chain PFAS) has {self.solubility} water solubility and {self.bioaccumulation_potential} bioaccumulation potential. "
                "It tends to bind strongly to soil and organic matter, leading to long-term environmental persistence.")

class ShortChainPFAS(PFASCompound):
    """Subclass representing short-chain PFAS (CF2 count <= 7)."""

    def __init__(self, name, cf2_count):
        super().__init__(name, cf2_count)
        self.solubility = "High"
        self.bioaccumulation_potential = "Low"

    @override
    def environmental_impact(self) -> str:
        """Describes the environmental impact of short-chain PFAS."""
        return (f"{self.name} (Short-Chain PFAS) has {self.solubility} water solubility and {self.bioaccumulation_potential} bioaccumulation potential. "
                "It is more mobile in groundwater, increasing the risk of widespread contamination.")

def classify_pfas(name, cf2_count):
    """
    Classifies a PFAS compound as either long-chain or short-chain based on CF2 count.
    :param name: Name of the PFAS compound.
    :param cf2_count: Number of CF2 groups.
    :return: An instance of LongChainPFAS or ShortChainPFAS.
    """
    if cf2_count > 7:
        return LongChainPFAS(name, cf2_count)
    else:
        return ShortChainPFAS(name, cf2_count)

# Example PFAS Compounds
pfoa = classify_pfas("PFOA (Perfluorooctanoic Acid)", 8)  # Long-chain PFAS (C8)
pfos = classify_pfas("PFOS (Perfluorooctane Sulfonate)", 8)  # Long-chain PFAS (C8)
pfba = classify_pfas("PFBA (Perfluorobutanoic Acid)", 4)  # Short-chain PFAS (C4)
pfhx = classify_pfas("PFHxA (Perfluorohexanoic Acid)", 6)  # Short-chain PFAS (C6)

# Printing Descriptions
pfas_list = [pfoa, pfos, pfba, pfhx]

for pfas in pfas_list:
    print(pfas.describe())  # General description
    print(pfas.environmental_impact())  # Environmental impact analysis
    print("-" * 80)

