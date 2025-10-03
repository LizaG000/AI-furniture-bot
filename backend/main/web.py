from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from backend.main.config import config
from backend.presentation.fastapi.setup import setup_routes
from backend.main.container import container

app = FastAPI(
    title=config.api.project_name
)

setup_routes(app, config)
setup_dishka(container, app)
