from pathlib import Path
from typing import Annotated
from uuid import uuid4
from dependencies.app import AppContainer
from redis import ConnectionPool
from taskiq_aio_pika import AioPikaBroker
from toml import load

from api.meals.tasks import MealsTasks


from taskiq import TaskiqEvents, TaskiqState


CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG = load(file)

global app_container
app_container = AppContainer(config=CONFIG)


def get_db():
    db = uuid4()
    return db


global db
db = get_db()
