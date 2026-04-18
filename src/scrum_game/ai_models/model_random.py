from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
import random
from src.scrum_game.utils.logger import log

class ModelRandom(AIBaseModel):

    def __int__(self):
        pass

    def get_action(self, game_state:GameState, actions:list[Action]):
        action_chosen = actions[random.randint(0, len(actions) - 1)]
        log(f"The action choosen is {action_chosen}") 
        return action_chosen