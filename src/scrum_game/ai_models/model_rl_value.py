from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
import numpy as np
import random

class ModelRLValue(AIBaseModel):
    """Value-based Reinforcement Learning Model"""
    
    def __init__(self, learning_rate=0.1, discount_factor=0.95, exploration_rate=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}  # Dictionary to store state -> {action: value}
    
    def extract_state_features(self, game_state: GameState) -> np.ndarray:
        """Convert GameState to simple feature vector"""
        player = game_state.players[game_state.current_turn]
        
        features = [
            player.balance / 100000,  # Normalize
            player.debt / 100000,
            game_state.sprint / 10,
        ]
        return np.array(features)
    
    def get_action(self, game_state: GameState, actions_list: list[Action]) -> Action:
        """Choose action using epsilon-greedy strategy"""
        state_key = tuple(self.extract_state_features(game_state))
        
        # Exploration: random action
        if np.random.random() < self.exploration_rate:
            return random.choice(actions_list)
        
        # Exploitation: best known action
        if state_key in self.q_table:
            best_action = max(self.q_table[state_key], key=self.q_table[state_key].get)
            if best_action in actions_list:
                return best_action
        
        # Default: random if unseen state
        return random.choice(actions_list)
    
    def update_learning(self, state_features, action, reward, next_state_features):
        """Learn from experience using Q-Learning"""
        state_key = tuple(state_features)
        next_key = tuple(next_state_features)
        
        # Initialize state if new
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        
        # Get current estimate
        current_estimate = self.q_table[state_key].get(action, 0)
        
        # Get best future value
        next_actions = self.q_table.get(next_key, {})
        best_future = max(next_actions.values()) if next_actions else 0
        
        # Q-Learning update
        new_estimate = current_estimate + self.learning_rate * (reward + self.discount_factor * best_future - current_estimate)
        self.q_table[state_key][action] = new_estimate
        
        # Only log big rewards
        if abs(reward) > 1000:  # Only log big rewards
            print(f"State: {state_key}, Action: {action}, Reward: {reward}")