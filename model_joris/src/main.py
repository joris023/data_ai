import socket
import json
import time

from services.logger import log
from models.game_state import GameState
from services.model import get_action

def connect_to_server() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)
    client.connect(('127.0.0.1', 9999))

    # Confirm connections
    client.send(b"Hello from client (Confirming connection)")
    log(client.recv(1024).decode(), source="Server")
    return client

def run_model(client: socket.socket) -> None:
    while True:
        try:
            time.sleep(1)
            log("Waiting to recieve data (state) from Server")
            data = client.recv(4096)
            game_state_dict = json.loads(data.decode())
            game_state = GameState.from_dict(game_state_dict)
            log("Recieved the state", source="Server")

            log("Calculating action")
            action = get_action(game_state)

            time.sleep(1)
            log(f"Sending {action} action to Server")
            client.sendall(b"Action A")
            
        except Exception as e:
            log(f"Connections failed: {e}")
            break

if __name__ == "__main__":
    log("This is Joris model running")
    client = connect_to_server()
    run_model(client)