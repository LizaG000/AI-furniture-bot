from dishka import make_async_container
from backend.main.provider import MainProvider
from backend.infra.postgres.provider import PostgresProvider
from backend.config import Config
from backend.main.config import config

container = make_async_container(
    MainProvider(),
    PostgresProvider(),
    context={
        Config: config
    }
)