from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.models.game_state import GameState
from src.scrum_game.models.enums.action import Action
from collections import defaultdict
import numpy as np
import random
from src.scrum_game.models.dqn import DQN
from src.scrum_game.models.position import Position
import torch
import torch.nn as nn
from .utils.experience_replay import ExperienceReplay

device = 'cuda' if torch.cuda.is_available() else 'cpu'
ALL_ACTIONS = list(Action)

class ModelValue(AIBaseModel):
    
    def __init__(self, player_amount:int):
        state_dim = 82 + (3 * player_amount)
        self.dqn = DQN(state_dim=state_dim, action_dim=6).to(device)

        learning_rate = 1e-3
        self.optimizer = torch.optim.Adam(self.dqn.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()

        self.replay_memory = ExperienceReplay(10_000)
        self.batch_size = 32

        # Bepaald hoe belangrijk de toekomst is (discount factor)
        self.gamma = 0.9

        # Bepaald exploration
        self.epsilon = 1
        self.epsilon_decay = 0.97
        self.epsilon_min = 0.05

        self.losses = []

    def extract_state_features(self, game_state: GameState) -> np.ndarray:
        # Flatten de state en scale alle features (Mischien later aanpassen aangezien somige dingen belangrijker zijn dan andere)
        vec = []

        vec.append(game_state.current_turn)
        vec.append(game_state.sprint / 5.0)

        for p in game_state.players:
            vec.append((p.balance - p.debt) / 100_000.0)
            vec.append((p.position.product or 0) / 5.0)
            vec.append((p.position.sprint or 0) / 4.0)

        for product in range(1, 6):
            for sprint in range(1, 5):
                pos = Position(product, sprint)
                field = game_state.board[pos]

                vec.append(pos.product / 5.0)
                vec.append(pos.sprint / 4.0)
                vec.append(field.features / 4.0)
                vec.append(field.rings / 10.0)

        return np.array(vec, dtype=np.float32)
    


    def get_action(self, game_state: GameState, actions: list[Action]) -> Action:

        state = self.extract_state_features(game_state)
        state = torch.tensor(state, dtype=torch.float, device=device)

        if random.random() < self.epsilon:
            action = random.choice(actions)
        else:
            with torch.no_grad(): 
                # Pak alle q-values
                q_values = self.dqn(state.unsqueeze(dim=0)).squeeze(dim=0)
                
                # Maak ongeldige actions -inf
                valid_indices = [ALL_ACTIONS.index(a) for a in actions]
                mask = torch.full(q_values.shape, float('-inf'), device=device)
                mask[valid_indices] = q_values[valid_indices]

                # Kies de action met hoogste q-value
                action = ALL_ACTIONS[mask.argmax().item()]
        
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
        
        return action



    def learn(self, old_game_state:np.ndarray, action:Action, new_game_state:GameState, reward:float) -> None:
        
        new_state = self.extract_state_features(new_game_state)
        action_idx = ALL_ACTIONS.index(action)

        self.replay_memory.append((old_game_state, action_idx, reward, new_state))

        if len(self.replay_memory) >= self.batch_size:
            self._update_learning()



    def _update_learning(self) -> None:
        batch = self.replay_memory.sample(self.batch_size)

        # Maak alles naar tensors
        old_states = torch.tensor(np.array([t[0] for t in batch]), dtype=torch.float, device=device)
        actions = torch.tensor([t[1] for t in batch], dtype=torch.long, device=device)
        rewards = torch.tensor([t[2] for t in batch], dtype=torch.float, device=device)
        new_states = torch.tensor(np.array([t[3] for t in batch]), dtype=torch.float, device=device)

        # Q(S,A) van gekozen action + state
        current_q = self.dqn(old_states).gather(1, actions.unsqueeze(dim=1)).squeeze(dim=1)

        # Pak alle Q-values van de opvolgende state en bereken wat de juiste Q-values hadden moeten zijn
        with torch.no_grad():
            next_q = self.dqn(new_states).max(dim=1).values
            target_q = rewards + self.gamma * next_q

        loss = self.loss_fn(current_q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.losses.append(loss.item())

    def _sav_weights(self):
        pass # ToDo

    def _load_weights(self):
        pass # ToDo