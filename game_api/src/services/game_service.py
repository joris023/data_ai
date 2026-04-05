import time
import socket
import random
from models.game_state import GameState
import json
from.logger import log

class GameService():
    
    def __init__(self, connections:list[socket.socket]):
        self._connections = connections
        self.sprints = 6
        self.players = {player_id: client for player_id, client in enumerate(connections)}
        self.game_state = GameState.create_game_state(self.players)
        

    def start(self):
        time.sleep(2)
        log(f"Starting new game with {len(self._connections)} players connected.")
        
        for i in range(self.sprints):
            log(f"Starting sprint {i+1}")
            
            for player_id in sorted(self.players.keys()):
                try:
                    time.sleep(2)
                    log(f"Sending data (state) to model {player_id}")
                    data = (json.dumps(self.game_state.to_dict())).encode()
                    self.players[player_id].send(data)

                    time.sleep(2)
                    log(f"Waiting on response from Model {player_id}")
                    response = self.players[player_id].recv(1024).decode()
                    log(f"{response} action recieved", source=f"Model_{player_id}")

                except Exception as e:
                    log(f"Connection failed: {e}", level="ERROR")
                    self._remove_player_from_game(player_id)
                
    
    def _remove_player_from_game(self, player_id):
        client = self.players.get(player_id)
        if not client:
            return

        if client in self._connections:
            self._connections.remove(client)
        if player_id in self.players:
            self.players.pop(player_id)
        if player_id in self.game_state.players:
            self.game_state.players.pop(player_id)
        log(f"Remove player {player_id} from the game")
    