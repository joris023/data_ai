from dataclasses import dataclass
from src.scrum_game.models.player import Player
from src.scrum_game.models.field import Field
from src.scrum_game.models.enums.action import Action
from src.scrum_game.models.position import Position
from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from .data import default_board
import random

# 1.
@dataclass
class GameState():
    current_turn: int
    sprint: int
    players: list[Player]
    board: list[Field]

    def __init__(self, ai_models:list[AIBaseModel]) -> None:
        self.current_turn = 0
        self.sprint = 0
        self.players = [Player(position=Position(None, None), balance=30_000, debt=0, model=model) for model in ai_models]
        self.board = default_board

    def reset(self) -> None:
        self.sprint = 0
        self.current_turn = 0
        for player in self.players:
            player.balance = 30_000
            player.debt = 0
            player.position = Position(None, None)
        self.board = default_board

    # TAAK
    def update_state(self, action:Action):
        
        player = self.players[self.current_turn]
        
        self._apply_action(player, action)

    def _apply_action(self, player:Player, action:Action) -> None:

        match action:
            case Action.SWITCH01:
                player.position.product = 1
            case Action.SWITCH02:
                player.position.product = 2
            case Action.SWITCH03:
                player.position.product = 3
            case Action.SWITCH04:
                player.position.product = 4
            case Action.SWITCH05:
                player.position.product = 5
            case Action.SWITCH06:
                player.position.product = 6
            case Action.STAY:
                player.position.sprint += 1
            case _:
                pass
        
        if action != Action.STAY:
            player.balance -= 5_000
            player.position.sprint = 1

    def _roll_dice(field:Field) -> None:
        
        # Dobbel je 
        # Krijg je geld of niet postive verlies je geld
        # als die geld afgaat en negative dan leent die automatisch
        pass


    def __str__(self):
        result = f"\n{'='*60}\nSPRINT {self.sprint} - CURRENT TURN {self.current_turn}\n{'='*60}\n"

        # Print Players
        result += "PLAYERS:\n"
        for i, player in enumerate(self.players):
            result += f"{i}. {player}\n"

        result += f"\nBOARD ({len(self.board)} fields):\n"
        
        # Print Board
        for field in self.board:
            result += f"{field}\n"
        result += "="*60
        return result