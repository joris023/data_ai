import fastapi
from src.scrum_game.models.dto.action_response_dto import ActionResponseDTO
from src.scrum_game.models.dto.game_state_dto import GameStateDTO
from src.scrum_game.ai_models.ai_base_model import AIBaseModel
from src.scrum_game.services.state_service import StateService

router = fastapi.APIRouter(prefix="/state")

@router.post(
    path="",
    response_model=ActionResponseDTO
)
def post_state(state:GameStateDTO):

    state_service = StateService()
    action = state_service.get_action(state)
    return ActionResponseDTO(action)