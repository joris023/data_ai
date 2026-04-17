from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_joris import ModelJoris
from src.scrum_game.ai_models.model_policy import ModelPolicy
from src.scrum_game.ai_models.model_rl_value import ModelRLValue
import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

def _get_models(amount_of_players:int, model_name:str) -> list:

    models = []
    for _ in range(amount_of_players):
        match model_name:
            case "joris":
                models.append(ModelJoris())
            case "policy":
                models.append(ModelPolicy())
            case "lucas":
                pass
            case "wesley":
                pass
            case "wouter":
                pass
            case "rl_value":
                models.append(ModelRLValue())
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
    player_net_history = [[] for _ in range(amount_of_players)]
    average_game_nets = []
    
    print(f"Running {runs} games with model {model_name} and {amount_of_players} players")
    for game_index in range(runs):
        print(f"Starting game {game_index + 1}/{runs}")
        game_service.start()

        game_nets = [player.balance - player.debt for player in game_service.game_state.players]
        average_game_nets.append(np.mean(game_nets))
        for player_index, net in enumerate(game_nets):
            player_net_history[player_index].append(net)

        game_service.reset()

    mean = np.mean(average_game_nets)
    print(mean)

    # Create performance graph
    plt.figure(figsize=(10, 6))
    game_numbers = np.arange(1, runs + 1)
    plt.plot(game_numbers, average_game_nets, marker='o', linestyle='None', alpha=0.7, label='Average net balance')

    for player_index, history in enumerate(player_net_history):
        if amount_of_players <= 5:
            plt.plot(game_numbers, history, marker='x', linestyle='None', alpha=0.6, label=f'Player {player_index + 1}')

    # Add a linear regression trend line to show improvement
    if runs > 1:
        coeffs = np.polyfit(game_numbers, average_game_nets, deg=1)
        trend_line = np.poly1d(coeffs)
        plt.plot(game_numbers, trend_line(game_numbers), color='green', linestyle='--', linewidth=2, label='Trend line')

    # Add a moving-average line to smooth short-term noise
    if runs >= 3:
        window = max(3, runs // 10)
        moving_avg = np.convolve(average_game_nets, np.ones(window) / window, mode='valid')
        avg_numbers = np.arange(window, runs + 1)
        plt.plot(avg_numbers, moving_avg, color='orange', linestyle='-', linewidth=2, alpha=0.9, label=f'{window}-game moving avg')

    plt.title(f'{model_name.capitalize()} Model Performance Over {runs} Games')
    plt.xlabel('Game Number')
    plt.ylabel('Average Net Balance (€)')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=mean, color='red', linestyle='--', label=f'Mean: €{mean:,.0f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
    print("Graph saved as 'training_results.png'")