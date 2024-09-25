import logging
import logging.config
from pathlib import Path
from pprint import pformat
from typing import Literal, Union

from pydantic import BaseModel, HttpUrl, PostgresDsn
from toml import load

from src.config.validation import validate_config

BASE_DIR_PATH = Path.cwd()
CONFIG_FILE_PATH = Path(__file__).parent / "config.toml"

with open(CONFIG_FILE_PATH, "r") as file:
    CONFIG_DICT = load(file)
    uris = validate_config(CONFIG_DICT)
    
    CONFIG_DICT["dns"]["timescaledb"]["uri"] = uris["uri_timescale_db"]
    CONFIG_DICT["dns"]["eventstoredb"]["uri"] = uris["uri_event_store_db"]
    CONFIG_DICT["dns"]["rabbitmq"]["uri"] = uris["uri_rabbit_mq"]


def get_module_path(file: str):
    return (
        Path(file)
        .resolve()
        .relative_to(BASE_DIR_PATH)
        .with_suffix("")
        .as_posix()
        .replace("/", ".")
    )


def setup_logging():
    logging.config.dictConfig(CONFIG_DICT["logging"])
