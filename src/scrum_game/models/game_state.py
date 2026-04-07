from dataclasses import dataclass
from scrum_game.models.player import Player
from scrum_game.models.field import Field
from scrum_game.models.enums.action import Action

@dataclass
class GameState():
    round: int
    players: list[Player]
    board: list[Field]


    def update_state(action: Action):
        pass
