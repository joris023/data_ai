from dataclasses import dataclass
from src.scrum_game.models.player import Player
from src.scrum_game.models.field import Field
from src.scrum_game.models.enums.action import Action
from src.scrum_game.models.position import Position
from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.utils.logger import log
from .data import default_board
import random

# 1.
@dataclass
class GameState():
    current_turn: int
    sprint: int
    players: list[Player]
    board: dict[Position, Field]

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
    def update_state(self, action:Action|None=None):

        if self.sprint != 0:
            self._roll_dice()
            self._draw_refinment_card()
        if action:
            self._apply_action(action)
            
        self._check_balance()
        



    def _roll_dice(self) -> None:
        
        player = self.players[self.current_turn]
        field = self.board[player.position]

        features = field.features
        rings = field.rings

        score = 0
        
        for _ in range(5):
            match features:
                case 1:
                    roll = random.randint(1, 20)
                case 2:
                    roll = random.randint(1, 10) + random.randint(1, 10)
                case 3 | 4:
                    roll = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
            score += roll - 12

        total = 0
        if score > 0:
            total -= (score * 1_000)
        else:
            total += (rings * 5_000) + (score * 1000)

        log(f"Had a balance of {player.balance} scored: {score} rings: {rings} so {total} recieved")
        player.balance += total
        log(f"Updated balance = {player.balance}")

    

    def _check_balance(self):
        player = self.players[self.current_turn]

        while player.balance < 0:
            player.debt += 50_000
            player.balance += 50_000



    def _apply_action(self, action:Action) -> None:
        player = self.players[self.current_turn]
        match action:
            case Action.SWITCH01:
                player.position = Position(product=1, sprint=player.position.sprint)
            case Action.SWITCH02:
                player.position = Position(product=2, sprint=player.position.sprint)
            case Action.SWITCH03:
                player.position = Position(product=3, sprint=player.position.sprint)
            case Action.SWITCH04:
                player.position = Position(product=4, sprint=player.position.sprint)
            case Action.SWITCH05:
                player.position = Position(product=5, sprint=player.position.sprint)
            case Action.STAY:
                player.position = Position(product=player.position.product, sprint=player.position.sprint + 1)
            case _:
                pass
        
        if action != Action.STAY:
            player.balance -= 5_000
            player.position = Position(product=player.position.product, sprint=1)



    def draw_incident_card(self):
        
        product = random.randint(1, 5)
        score = random.randint(-5, 5)        

        for sprint in range(4):
            field = self.board[Position(product=product, sprint=sprint+1)]
            field.rings += score
            if field.rings < 0: field.rings = 0
        
        log(f"Product changed = {product}, change with {score} rings.")



    def _draw_refinment_card(self):
        player = self.players[self.current_turn]
        field = self.board[player.position]

        score = random.randint(-2, 2)
        field.features += score
        
        if field.features < 1: field.features = 1
        elif field.features > 4: field.features = 4

        log(f"Product/Sprint changed = P{player.position.product}:S{player.position.sprint}, change with {score} features. Result {field.features} features")



    def __str__(self):
        # Print Players
        result = "\nPLAYERS:\n"
        for i, player in enumerate(self.players):
            result += f"{i}. {player}\n"

        result += f"\nBOARD ({len(self.board)} fields):\n"
        
        # Print Board
        for position, field in self.board.items():
            result += f"{position} - {field}\n"
        result += "="*60
        return result