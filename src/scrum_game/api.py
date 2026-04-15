import os
import uvicorn
from src.scrum_game.controllers.state_controller import router as state_router
import fastapi

app = fastapi.FastAPI()
app.include_router(state_router)

if __name__ == "__main__":
    use_api = bool(os.environ.get("USE_API"))
    model_name = str(os.environ.get("MODEL"))

    uvicorn.run("src.scrum_game.api:app", reload=True)