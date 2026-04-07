from dataclasses import dataclass
from scrum_game.models.player import Player
from scrum_game.models.field import Field
from scrum_game.models.enums.action import Action
import random

# 1.
@dataclass
class GameState():
    round: int
    players: list[Player]
    board: list[Field]

    # TAAK
    def update_state(action: Action):
        pass

        
        nummer = random.randint(1, 20)
        # Dobbel je 
        # Krijg je geld of niet postive verlies je geld
        # als die geld afgaat en negative dan leent die automatisch
        # Actie de player bewegen 
        # Betalen als switch
