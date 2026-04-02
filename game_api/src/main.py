import socket
import time
import threading
from fastapi import FastAPI
import uvicorn
# from gamesrc.services.game_service import GameService
from services.game_service import GameService

app = FastAPI()

CONNECTIONS = []
STARTED = False

def get_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(4)

    while True:
        client, address_client = server.accept()
        CONNECTIONS.append(client)
            
        # VERWIJDER CLIENTS UIT CONNECTIONS VAN CLIENT DIE ZIJN GE DISCONNECT
        print(client.recv(1024).decode())
        client.send("Hello from server".encode())

def game_loop():
    while True:
        while STARTED:
            game = GameService(connections=CONNECTIONS)
            game.start()

@app.get("/start")
def start_game():
    global STARTED
    STARTED = True
    return {"message": "Game started"}

@app.get("/stop")
def stop_game():
    global STARTED
    STARTED = False
    return {"message": "Game started"}

if __name__ == "__main__":

    print("This is the Game API")

    threading.Thread(target=get_connections, daemon=True, name="get_connections").start()
    threading.Thread(target=game_loop, daemon=True, name="game_loop").start()  

    uvicorn.run(app, host="127.0.0.1", port=8000)








# # state bijhouden
# state = None

# INit elke speler krijg een player id
# for p in range(len(players)):
#     init(p)


# # For elke sprint
# For i in range(6):
    
#     # For elke speler
#     For p in range(len(player)):
        
#         # verstuur de state
#         send(p, state)
        
#         # krijg de action die de speler koos
#         action <- player

#         # update de state
#         update(state, action)
#         insert_in_db(state)