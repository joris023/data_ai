from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_joris import ModelJoris
import os
from dotenv import load_dotenv
import numpy as np

def _get_models(amount_of_players:int, model_name:str) -> list:

    models = []
    for _ in range(amount_of_players):
        match model_name:
            case "joris":
                models.append(ModelJoris())
            case "luciano":
                pass
            case "lucas":
                pass
            case "wesley":
                pass
            case "wouter":
                pass
            case "random":
                pass
            case _:
                raise ValueError(f"Model {model_name} not recognized")
    return models

load_dotenv()
if __name__ == "__main__":
    runs = int(os.environ.get("RUNS"))
    model_name = str(os.environ.get("MODEL"))
    amount_of_players = int(os.environ.get("AMOUNT_OF_PLAYERS"))
    
    models = _get_models(amount_of_players, model_name)
    
    game_service = GameService(models)
    end_balances = []
    
    print(f"Running {runs} games with model {model_name} and {amount_of_players} players")
    for _ in range(runs):
        
        game_service.start()
        for player in game_service.game_state.players:
            end_balances.append(player.balance - player.debt)

        game_service.reset()

    mean = np.mean(end_balances)
    print(mean)