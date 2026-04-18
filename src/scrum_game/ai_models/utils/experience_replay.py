from collections import deque
import random
import numpy as np

class ExperienceReplay():
    def __init__(self, maxlen:int, seed=None):
        self.memory = deque([], maxlen=maxlen)

        if seed is not None:
            random.seed(seed)
    
    # transition = (old_state, action_idx, reward, new_state)
    def append(self, transition:tuple[np.ndarray, int, float, np.ndarray]) -> None:
        self.memory.append(transition)

    def sample(self, sample_size:int) -> list[tuple]:
        return random.sample(self.memory, sample_size)
    
    def __len__(self) -> int:
        return len(self.memory)