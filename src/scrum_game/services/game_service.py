from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
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
                print(f"\n\n\n{'='*60}\nSPRINT {sprint} - CURRENT TURN {turn}\n{'='*60}\n")
                self._execute_player_turn(player, sprint)

                print(self.game_state)
            
            self.game_state.draw_incident_card()
        print(f"\n\n\n{'='*60}\nFINAL SPRINT (6)\n{'='*60}\n")    
        for turn, player in enumerate(self.game_state.players):
            self.game_state.current_turn = turn
            self.game_state.update_state()

        winner = None 
        print("\n FINAL BALANCES:")
        for player in self.game_state.players:
            print(f"Player {self.game_state.players.index(player) + 1} - Balance: {player.balance}, Debt: {player.debt}, Net: {player.balance - player.debt}")
            if not winner or player.balance > winner.balance:
                winner = player
        print(f"\n{'='*60}\nWINNER : {winner}\n{'='*60}\n")            
                
    def reset(self):
        self.game_state.reset()

    def _get_possible_actions(self, player:Player, round:int):
        actions_list = [action for action in Action]
        if round == 0 or player.position.sprint == 4:
            actions_list.remove(Action.STAY)
        return actions_list

    def _execute_player_turn(self, player: Player, sprint: int):
        """Execute a player's turn and handle learning if applicable"""
        balance_before = player.balance
    
        # Extract state before if model supports learning
        if hasattr(player.model, 'extract_state_features'):
            state_before = player.model.extract_state_features(self.game_state)
        else:
            state_before = None

        # Get and execute action
        actions = self._get_possible_actions(player, sprint)
        action = player.model.get_action(game_state=self.game_state, actions_list=actions)
        self.game_state.update_state(action)

        # Handle learning if model supports it
        if state_before is not None and hasattr(player.model, 'update_learning'):
            balance_after = player.balance
            state_after = player.model.extract_state_features(self.game_state)
            reward = balance_after - balance_before
            player.model.update_learning(state_before, action, reward, state_after)