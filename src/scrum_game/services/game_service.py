from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.utils.logger import log
from src.scrum_game.models.player import Player
from src.scrum_game.models.enums.action import Action

class GameService():

    def __init__(self, ai_models:list[AIBaseModel]):
        self.game_state = GameState(ai_models)

    def start(self):
        sprints = 6  #6 rounds + init round
        for sprint in range(sprints):
            self.game_state.sprint = sprint

            for turn, player in enumerate(self.game_state.players):
                self.game_state.current_turn = turn

                actions = self._get_possible_actions(player, sprint)
                action = player.model.get_action(game_state=self.game_state, actions_list=actions)
                self.game_state.update_state(action)
                print(self.game_state)
        
        for turn, player in enumerate(self.game_state.players):
            self.game_state.current_turn = turn
            self.game_state.update_state()
            

        # EVALUATE WINNER
                
    def reset(self):
        self.game_state.reset()

    def _get_possible_actions(self, player:Player, round:int):
        actions_list = [action for action in Action]
        if round == 0 or player.position.sprint == 4:
            actions_list.remove(Action.STAY)
        return actions_list