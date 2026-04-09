from dataclasses import dataclass

@dataclass
class Position():
    product: int
    sprint: int

    def __str__(self):
        return f"Pos(P{self.product}:S{self.sprint})"

    def __repr__(self):
        return f"Position(product={self.product}, sprint={self.sprint})"