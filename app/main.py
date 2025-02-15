import logging.config

from app.logging_setup import logging_setup

# import json

logger = logging.getLogger(__name__)


def main() -> None:
    print("123123123")
    logging_setup()
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
