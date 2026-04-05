from .field import Field

class GameState():
    def __init__(
        self,
        sprint:int,
        current_turn_player_id:int,
        board:dict[str,Field],
        players:dict[str:dict]
    ) -> None:
        self.sprint = sprint
        self.current_turn_player_id = current_turn_player_id
        self.board = board
        self.players = players

    @staticmethod
    def from_dict(data):
        return GameState(
            sprint=data["sprint"],
            current_turn_player_id=data["current_turn_player_id"],
            board={k: Field.from_dict(v) for k, v in data["board"].items()},
            players=data["players"]
        )