import atexit
import logging.config
import tomllib
from logging import Handler
from pathlib import Path

# import json

logger = logging.getLogger(__name__)

# def setup_logging():
#     config_file = Path(".logging_configs/base_config.json")
#     with open(config_file) as file:
#         config = json.load(file)
#     logging.config.dictConfig(config)

#     queue_handle = logging.getHandlerByName("queue_handler")
#     if queue_handle is not None:
#         queue_handle.listener.start()
#         atexit.register(queue_handle.listener.stop)


def setup_logging() -> None:
    config_file = Path(".logging_configs/config.toml")
    with open(config_file, "rb") as file:
        config = tomllib.load(file)
    logging.config.dictConfig(config)

    queue_handle: Handler | None = logging.getHandlerByName("queue_handler")
    if queue_handle is not None:
        queue_handle.listener.start()  # type: ignore [attr-defined]
        atexit.register(queue_handle.listener.stop)  # type: ignore [attr-defined]


def main() -> None:
    setup_logging()
    # logging.config.dictConfig(l/ogging_config)
    # logging.basicConfig(level=logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
