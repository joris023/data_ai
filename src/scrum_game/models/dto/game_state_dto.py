from pydantic import BaseModel, ConfigDict
from src.scrum_game.models.player import Player
from src.scrum_game.models.position import Position
from src.scrum_game.models.field import Field
from src.scrum_game.models.game_state import GameState
from src.scrum_game.ai_models.ai_base_model import AIBaseModel

class GameStateDTO(BaseModel):
    ai_model_name: str
    is_init: bool
    current_turn: int
    sprint: int
    players: list[dict] # list[list[dict[postion dict[product, sprint], balance, dept]]]
    board: list[dict] # list[list[ dict[postion:]]

    def convert_to_normal(self) -> GameState:
        # Players
        players = [
            Player(
                position=Position(**p["position"]),
                balance=p["balance"],
                debt=p["debt"],
                model=None  # later koppelen via ai_model_name
            )
            for p in self.players
        ]

        # Board
        board = {
            Position(**entry["position"]): Field(**entry["field"])
            for entry in self.board
        }

        # GameState init (jouw constructor verwacht ai_models)
        game_state = GameState(ai_models=[])

        game_state.players = players
        game_state.board = board
        game_state.current_turn = self.current_turn
        game_state.sprint = self.sprint

        return game_state
