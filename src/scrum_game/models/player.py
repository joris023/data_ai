from dataclasses import dataclass
from src.scrum_game.models.position import Position
from src.scrum_game.ai_models.ai_base_model import AIBaseModel

@dataclass
class Player():
    position: Position
    balance: int
    debt: int
    model: AIBaseModel | None = None

    def __str__(self):
        net = self.balance - self.debt
        return f"Player({self.position} | €{self.balance:,} - €{self.debt:,} = €{net:,})"

    def __repr__(self):
        return f"Player(position={self.position!r}, balance={self.balance}, debt={self.debt})"