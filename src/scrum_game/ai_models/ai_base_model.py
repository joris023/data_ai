from abc import ABC

class AIBaseModel(ABC):

    def get_action(self, game_state, actions):
        pass

    def learn(self, old_game_state, action, new_game_state, reward):
        pass

    def extract_state_features(self, game_state):
        pass