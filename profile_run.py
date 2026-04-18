"""Run dit met: python profile_run.py
Draait 100 games en laat zien waar de tijd heen gaat."""

import cProfile
import pstats
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["RUNS"] = "100"

def run():
    from src.scrum_game.services.game_service import GameService
    from src.scrum_game.ai_models.model_value import ModelValue

    amount_of_players = 2
    models = [ModelValue(amount_of_players) for _ in range(amount_of_players)]
    game_service = GameService(models)

    for i in range(100):
        game_service.start()
        game_service.reset()

cProfile.run('run()', 'profile_output')

stats = pstats.Stats('profile_output')
stats.strip_dirs()
stats.sort_stats('cumulative')
print("\n" + "="*80)
print("TOP 25 FUNCTIES (gesorteerd op cumulatieve tijd)")
print("="*80)
stats.print_stats(25)

print("\n" + "="*80)
print("TOP 25 FUNCTIES (gesorteerd op eigen tijd)")
print("="*80)
stats.sort_stats('tottime')
stats.print_stats(25)
