from dataclasses import dataclass
from scrum_game.models.position import Position

@dataclass
class Player():
    position: Position
    balance: int
    debt: int