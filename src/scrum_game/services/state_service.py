from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.dto.game_state_dto import GameStateDTO
from scrum_game.ai_models.model_random import ModelJoris
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action

class StateService():

    def __init__(self):
        pass

    def get_action(self, state_request:GameStateDTO):
        model = self._get_model(state_request.ai_model_name)
        is_init = state_request.is_init
        game_state = state_request.convert_to_normal()

        actions_list = [action for action in Action]
        if is_init: 
            actions_list.remove(Action.STAY)

        action = model.get_action(game_state, actions_list)
        return action

    def _get_model(self, model_name:str) -> AIBaseModel:
        match model_name:
            case "joris":
                return ModelJoris()
            case "luciano":
                pass
            case "lucas":
                pass
            case "wesley":
                pass
            case "wouter":
                pass
            case "random":
                pass
            case _:
                raise ValueError(f"Model {model_name} not recognized")