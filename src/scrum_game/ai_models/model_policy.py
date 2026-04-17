import numpy as np
from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
import pickle
import os


class ModelPolicy(AIBaseModel):
    """Policy-based reinforcement learning model using a simple linear policy."""

    def __init__(self, learning_rate: float = 0.05, baseline_alpha: float = 0.01):
        self.learning_rate = learning_rate
        self.baseline_alpha = baseline_alpha
        self.action_space = [
            Action.SWITCH01,
            Action.SWITCH02,
            Action.SWITCH03,
            Action.SWITCH04,
            Action.SWITCH05,
            Action.STAY,
        ]
        self.action_to_index = {action: idx for idx, action in enumerate(self.action_space)}
        self.feature_dim = 6
        self.weights = np.zeros((len(self.action_space), self.feature_dim), dtype=float)
        self.bias = np.zeros(len(self.action_space), dtype=float)
        self.baseline = 0.0

    def extract_state_features(self, game_state: GameState) -> np.ndarray:
        player = game_state.players[game_state.current_turn]
        position = player.position

        if position.product is None or position.sprint is None:
            product_norm = 0.0
            sprint_norm = 0.0
            field_features = 1.0
            field_rings = 0.0
        else:
            field = game_state.board[position]
            product_norm = (position.product - 1) / 4
            sprint_norm = (position.sprint - 1) / 3
            field_features = (field.features - 1) / 3
            field_rings = field.rings / 20

        features = np.array([
            player.balance / 100000,
            player.debt / 100000,
            game_state.sprint / 10,
            product_norm,
            sprint_norm,
            field_features if field_features >= 0 else 0.0,
        ], dtype=float)

        return features

    def _logits(self, state_features: np.ndarray) -> np.ndarray:
        return np.dot(self.weights, state_features) + self.bias

    def _softmax(self, scores: np.ndarray) -> np.ndarray:
        shifted = scores - np.max(scores)
        exp_scores = np.exp(shifted)
        return exp_scores / np.sum(exp_scores)

    def get_action(self, game_state: GameState, actions_list: list[Action]) -> Action:
        state_features = self.extract_state_features(game_state)
        logits = self._logits(state_features)

        action_mask = np.array([1.0 if action in actions_list else 0.0 for action in self.action_space], dtype=float)
        masked_logits = np.where(action_mask > 0, logits, -1e9)

        probs = self._softmax(masked_logits)
        choice_index = np.random.choice(len(self.action_space), p=probs)
        return self.action_space[choice_index]

    def update_learning(self, state_features, action, reward, next_state_features):
        if action is None:
            return

        state_features = np.array(state_features, dtype=float)
        action_index = self.action_to_index[action]

        logits = self._logits(state_features)
        probs = self._softmax(logits)

        advantage = reward - self.baseline
        self.baseline += self.baseline_alpha * advantage

        advantage_term = self.learning_rate * advantage
        self.weights[action_index] += advantage_term * state_features
        self.bias[action_index] += advantage_term

        # Policy gradient update for the non-selected actions
        for idx in range(len(self.action_space)):
            if idx == action_index:
                continue
            self.weights[idx] -= self.learning_rate * probs[idx] * state_features
            self.bias[idx] -= self.learning_rate * probs[idx]

        if abs(reward) > 1000:
            print(f"Policy update: action={action}, reward={reward:.0f}, advantage={advantage:.3f}")

    def save_weights(self, filepath: str):
        """Save the model's weights to a file."""
        data = {
            'weights': self.weights,
            'bias': self.bias,
            'baseline': self.baseline,
            'learning_rate': self.learning_rate,
            'baseline_alpha': self.baseline_alpha
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Model saved to {filepath}")

    def load_weights(self, filepath: str):
        """Load weights from a file."""
        if not os.path.exists(filepath):
            print(f"No saved model found at {filepath}, starting fresh")
            return
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.weights = data['weights']
        self.bias = data['bias']
        self.baseline = data['baseline']
        # Optionally restore hyperparameters too
        print(f"Model loaded from {filepath}")
