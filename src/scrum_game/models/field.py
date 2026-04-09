from dataclasses import dataclass
from src.scrum_game.models.position import Position

@dataclass
class Field(Position):
    rings: int
    features: int

    def __str__(self):
        return f"Field(P{self.product}:S{self.sprint} | R{self.rings}:F{self.features})"

    def __repr__(self):
        return f"Field(product={self.product}, sprint={self.sprint}, rings={self.rings}, features={self.features})"