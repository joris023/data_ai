from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_joris import ModelJoris
import os
from dotenv import load_dotenv
import numpy as np
 
load_dotenv()
if __name__ == "__main__":
    runs = int(os.environ.get("RUNS"))
    model_name = str(os.environ.get("MODEL"))
    amount_of_players = int(os.environ.get("AMOUNT_OF_PLAYERS"))

    print(f"Running {runs} games with model {model_name} and {amount_of_players} players")

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

    game_service = GameService(models)
    end_balances = []
    for _ in range(runs):
        
        game_service.start()
        for player in game_service.game_state.players:
            end_balances.append(player.balance - player.debt)

        game_service.reset()

    mean = np.mean(end_balances)
    print(mean)
    