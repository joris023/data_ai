from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_random import ModelRandom
from src.scrum_game.ai_models.model_value import ModelValue
from src.scrum_game.utils.plotting import plot_results
import os
from dotenv import load_dotenv
import numpy as np

def _get_model(model_name: str, player_amount:int):
    model_name = model_name.split("_")[0]
    match model_name:
        case "random":
            return ModelRandom()
        case "value":
            return ModelValue(player_amount)
        case _:
            raise ValueError(f"Model {model_name} not recognized")


load_dotenv()
if __name__ == "__main__":
    runs = int(os.environ.get("RUNS"))
    model_names = [f"{n.strip()}_{i}" for i, n in enumerate(os.environ.get("MODELS").split(","))]

    models = [_get_model(name, len(model_names)) for name in model_names]
    game_service = GameService(models)

    results = {name: [] for name in model_names}

    print(f"Running {runs} games with models {model_names}")
    for i in range(runs):
        game_service.start()

        for j, name in enumerate(model_names):
            player = game_service.game_state.players[j]
            results[name].append(player.balance - player.debt)

        game_service.reset()

        # Loading screen
        pct = (i + 1) / runs * 100
        if (i + 1) % max(1, runs // 100) == 0:
            print(f"\r{pct:.0f}% done ({i+1}/{runs})", end="", flush=True)

    for name in model_names:
        print(f"\n{name} mean: {np.mean(results[name]):.0f}")
        print(f"{name} final result: {results[name][-1]:.0f}")

    plot_results(results, runs)