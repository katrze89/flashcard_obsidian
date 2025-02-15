import atexit
import logging.config
import os
import tomllib
from logging import Handler
from pathlib import Path

# import json


# def setup_logging():
#     config_file = Path(".logging_configs/base_config.json")
#     with open(config_file) as file:
#         config = json.load(file)
#     logging.config.dictConfig(config)

#     queue_handle = logging.getHandlerByName("queue_handler")
#     if queue_handle is not None:
#         queue_handle.listener.start()
#         atexit.register(queue_handle.listener.stop)


def logging_setup() -> None:
    if os.getenv("TESTS") == "1":
        return
    config_file = Path(__file__).parent.resolve() / ".logging_configs/config.toml"
    with open(config_file, "rb") as file:
        config = tomllib.load(file)
    logging.config.dictConfig(config)

    queue_handle: Handler | None = logging.getHandlerByName("queue_handler")
    if queue_handle is not None:
        queue_handle.listener.start()  # type: ignore [attr-defined]
        atexit.register(queue_handle.listener.stop)  # type: ignore [attr-defined]
