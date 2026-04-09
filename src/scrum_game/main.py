from src.scrum_game.services.game_service import GameService
from src.scrum_game.ai_models.model_joris import ModelJoris
 
if __name__ == "__main__":
    model_joris_1 = ModelJoris()
    model_joris_2 = ModelJoris()
    game_service = GameService([model_joris_1, model_joris_2])
    
    arg_1 = 1
    
    for _ in range(arg_1):
        
        game_service.start()
        game_service.reset()