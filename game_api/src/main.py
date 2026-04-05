import socket
import time
import threading
from fastapi import FastAPI
import uvicorn
from services.game_service import GameService
from services.logger import log

# API - for starting and stopping
app = FastAPI()
@app.get("/start")
def start_game():
    global STARTED
    STARTED = True
    return {"message": "Game started"}

@app.get("/stop")
def stop_game():
    global STARTED
    STARTED = False
    return {"message": "Game stopped"}

CONNECTIONS = []
STARTED = False

def get_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(4)

    while True:
        client, addr = server.accept()
        
        client.send(b"Hello from server (Confirmed connection)")
        log(client.recv(1024).decode(), source="Client")

        CONNECTIONS.append(client)

def game_loop():
    global STARTED
    while True:
        if STARTED:
            game = GameService(connections=CONNECTIONS)
            game.start()
            STARTED = False
        time.sleep(0.1)     


if __name__ == "__main__":
    log("This is the Game API")
    
    threading.Thread(target=get_connections, daemon=True, name="get_connections").start()
    threading.Thread(target=game_loop, daemon=True, name="game_loop").start()  
    
    uvicorn.run(app, host="127.0.0.1", port=8000)