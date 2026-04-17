import numpy as np
from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
from src.scrum_game.models.position import Position
import pickle
import os


class ModelPolicy(AIBaseModel):
    """Policy-based reinforcement learning model using a simple linear policy."""

    def __init__(self, learning_rate: float = 0.05, baseline_alpha: float = 0.05, entropy_bonus: float = 0.01):
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
        self.feature_dim = 12
        self.weights = np.zeros((len(self.action_space), self.feature_dim), dtype=float)
        self.bias = np.zeros(len(self.action_space), dtype=float)
        self.baseline = 0.0
        self.entropy_bonus = entropy_bonus
        self._trajectory: list[tuple[np.ndarray, Action]] = []

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

        # Rings at sprint 1 for each product — used to evaluate SWITCH targets
        product_s1_rings = np.array([
            game_state.board[Position(product=p, sprint=1)].rings / 20
            for p in range(1, 6)
        ], dtype=float)

        features = np.array([
            player.balance / 100000,
            player.debt / 100000,
            game_state.sprint / 10,
            product_norm,
            sprint_norm,
            field_features if field_features >= 0 else 0.0,
            field_rings,
            *product_s1_rings,
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
        """Buffer this step; actual weight update happens in end_episode."""
        if action is None:
            return
        self._trajectory.append((np.array(state_features, dtype=float), action))

    def end_episode(self, final_net_balance: float):
        """Update policy using the episode return (final net balance).

        Using the episode return instead of per-step reward fixes credit assignment:
        switching to a high-ring product is rewarded for all future rolls it enables,
        not just penalized for the immediate -5000 switch cost.
        """
        if not self._trajectory:
            return

        # Normalize return to ~[-1, 1] scale so gradients don't explode.
        # Max reasonable net balance is ~200k, so /100000 keeps values in range.
        normalized_return = final_net_balance / 100000.0

        advantage = normalized_return - self.baseline
        self.baseline += self.baseline_alpha * advantage

        # Divide by trajectory length so 6 steps don't multiply the update 6x
        n = len(self._trajectory)
        advantage_term = self.learning_rate * advantage / n

        for state_features, action in self._trajectory:
            action_index = self.action_to_index[action]
            logits = self._logits(state_features)
            probs = self._softmax(logits)

            self.weights[action_index] += advantage_term * state_features
            self.bias[action_index] += advantage_term

            for idx in range(len(self.action_space)):
                if idx == action_index:
                    continue
                self.weights[idx] -= advantage_term * probs[idx] * state_features
                self.bias[idx] -= advantage_term * probs[idx]

            # Entropy bonus: push all weights toward uniform to prevent over-commitment
            entropy_term = self.entropy_bonus / n
            for idx in range(len(self.action_space)):
                self.weights[idx] += entropy_term * probs[idx] * (1 - probs[idx]) * state_features
                self.bias[idx]    += entropy_term * probs[idx] * (1 - probs[idx])

        print(f"Episode end: return={final_net_balance:.0f}, advantage={advantage:.4f}, steps={n}")
        self._trajectory.clear()

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
