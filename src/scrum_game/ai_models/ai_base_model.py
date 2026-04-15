from abc import ABC

class AIBaseModel(ABC):

    def get_action(self, game_state, actions_list):
        pass