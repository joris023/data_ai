from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.player import Player
from src.scrum_game.models.enums.action import Action
from src.scrum_game.utils.printer import printer
import copy

class GameService():

    def __init__(self, ai_models:list[AIBaseModel]):
        self.game_state = GameState(ai_models)

    def start(self):
        sprints = 6  # 5 rounds + init round
        for sprint in range(sprints):
            self.game_state.sprint = sprint

            for turn, player in enumerate(self.game_state.players):
                self.game_state.current_turn = turn
                old_game_state = player.model.extract_state_features(self.game_state)
                printer(f"\n\n\n{'='*60}\nSPRINT {sprint} - CURRENT TURN {turn}\n{'='*60}\n")
                
                actions = self._get_possible_actions(player, sprint)
                
                action = player.model.get_action(game_state=self.game_state, actions=actions)
                reward = self.game_state.update_state(action)
                player.model.learn(old_game_state, action, self.game_state, reward)

                printer(self.game_state)
            
            self.game_state.draw_incident_card()

        printer(f"\n\n\n{'='*60}\nFINAL SPRINT (6)\n{'='*60}\n")    
        for turn, player in enumerate(self.game_state.players):
            self.game_state.current_turn = turn
            self.game_state.update_state()

        winner = None 
        for player in self.game_state.players:
            if not winner or player.balance - player.debt > winner.balance - winner.debt:
                winner = player
        printer(f"\n{'='*60}\nWINNER : {winner}\n{'='*60}\n")            
                
    def reset(self):
        self.game_state.reset()

    def _get_possible_actions(self, player:Player, round:int):
        actions_list = [action for action in Action]
        if round == 0 or player.position.sprint == 4:
            actions_list.remove(Action.STAY)
        return actions_list