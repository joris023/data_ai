from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
import random
from src.scrum_game.utils.logger import log

class ModelJoris(AIBaseModel):

    def __int__(self):
        pass

    def get_action(self, game_state:GameState, actions_list:list[Action]):
        action_chosen = actions_list[random.randint(0, len(actions_list) - 1)]
        log(f"The action choosen is {action_chosen}") 
        return action_chosen