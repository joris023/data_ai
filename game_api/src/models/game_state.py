from .field import Field
import random
import socket

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

    def update_state():
        pass

    def move_player():
        pass

    @staticmethod
    def create_game_state(players: dict[str, socket.socket]):
        products = ["1", "2", "3", "4", "5", "6"]
        sprints = ["a", "b", "c", "d"]

        board = {}
        for product in products:
            for sprint in sprints:
                board[f"{product}{sprint}"] = Field(rings=random.randint(1,6), features=random.randint(1,4))

        players = {player_id: None for player_id in players}

        return GameState(0, 0, board, players)

    def to_dict(self):
        return {
            "sprint": self.sprint,
            "current_turn_player_id": self.current_turn_player_id,
            "board": {k: v.to_dict() for k, v in self.board.items()},
            "players": self.players
        }