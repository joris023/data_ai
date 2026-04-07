from abc import ABC
from scrum_game.models.game_state import GameState

class AIBaseModel(ABC):

    def get_action(self, game_state:GameState):
        pass