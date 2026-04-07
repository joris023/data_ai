from dataclasses import dataclass
from scrum_game.models.position import Position

@dataclass
class Field(Position):
    rings: int
    features: int