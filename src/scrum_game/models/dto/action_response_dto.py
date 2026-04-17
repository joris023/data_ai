from dataclasses import dataclass
from src.scrum_game.models.enums.action import Action

@dataclass
class ActionResponseDTO():
    action: Action