from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from scrum_game.models.game_state import GameState

class GameService():

    def __init__(self):
        self.game_state = GameState()

    def start(self, models: list[AIBaseModel]):
        
        rounds = 6

        for i in range(rounds):

            for model in models:
                action = model.get_action(self.game_state)
                self.game_state.update_state(action)