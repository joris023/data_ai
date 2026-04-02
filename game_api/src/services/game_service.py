import time
import socket

class GameService():
    
    def __init__(self, connections:list[socket.socket]):
        self._connections = connections

    def start(self):
        time.sleep(5)
        print(f"STARTING NEW GAME WITH {len(self._connections)}")
        
        for client in self._connections:
            try:
                client.send(b"Hello you are in a game")
            except Exception as e:
                print(f"Error {e}")