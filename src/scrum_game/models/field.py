from dataclasses import dataclass

@dataclass
class Field():
    rings: int
    features: int

    def __str__(self):
        return f"Field(R{self.rings}:F{self.features})"

    def __repr__(self):
        return f"Field(rings={self.rings}, features={self.features})"