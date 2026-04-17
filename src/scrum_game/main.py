from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_joris import ModelJoris
from src.scrum_game.ai_models.model_policy import ModelPolicy
from src.scrum_game.ai_models.model_rl_value import ModelRLValue
import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

MODEL_COLORS = {
    "policy":  "royalblue",
    "random":  "tomato",
    "rl_value":"mediumpurple",
}

def _build_models() -> tuple[list, list[str]]:
    """Returns (models, labels) based on MODEL_* env vars."""
    entries = [
        ("policy",   int(os.environ.get("MODEL_POLICY",  0)), ModelPolicy),
        ("random",   int(os.environ.get("MODEL_RANDOM",  0)), ModelJoris),
        ("rl_value", int(os.environ.get("MODEL_VALUE",   0)), ModelRLValue),
    ]
    models, labels = [], []
    for name, count, cls in entries:
        for i in range(count):
            models.append(cls())
            suffix = f" #{i+1}" if count > 1 else ""
            labels.append(f"{name}{suffix}")
    return models, labels


load_dotenv()
if __name__ == "__main__":
    runs = int(os.environ.get("RUNS"))
    models, player_labels = _build_models()
    amount_of_players = len(models)

    game_service = GameService(models)
    player_net_history = [[] for _ in range(amount_of_players)]

    title = " vs ".join(dict.fromkeys(l.split(" #")[0] for l in player_labels))
    print(f"Running {runs} games: {title} ({amount_of_players} players)")

    for game_index in range(runs):
        print(f"Starting game {game_index + 1}/{runs}")
        game_service.start()
        for player_index, player in enumerate(game_service.game_state.players):
            player_net_history[player_index].append(player.balance - player.debt)
        game_service.reset()

    # Graph
    plt.figure(figsize=(12, 6))
    game_numbers = np.arange(1, runs + 1)
    window = max(3, runs // 100)

    for player_index, (history, label) in enumerate(zip(player_net_history, player_labels)):
        model_type = label.split(" #")[0]
        color = MODEL_COLORS.get(model_type)
        moving_avg = np.convolve(history, np.ones(window) / window, mode='valid')
        avg_numbers = np.arange(window, runs + 1)
        plt.plot(avg_numbers, moving_avg, linewidth=2, alpha=0.9, color=color, label=label)

        mean = np.mean(history)
        plt.axhline(y=mean, linestyle='--', linewidth=1, color=color,
                    label=f"{label} mean: €{mean:,.0f}")

    # Trend line for the first non-random model
    first_learner = next(
        (i for i, l in enumerate(player_labels) if l.split(" #")[0] != "random"), 0
    )
    if runs > 1:
        coeffs = np.polyfit(game_numbers, player_net_history[first_learner], deg=1)
        trend = np.poly1d(coeffs)
        plt.plot(game_numbers, trend(game_numbers), color='green', linestyle=':',
                 linewidth=1.5, label=f"{player_labels[first_learner]} trend")

    plt.title(f"{title} — {runs} games")
    plt.xlabel("Game")
    plt.ylabel("Net Balance (€)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
    print("Graph saved as 'training_results.png'")
