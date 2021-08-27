import sys

from hypercorn import Config
from hypercorn.logging import Logger

from helpers.log import log_create

LOG_CREATE_ACCESS = log_create(name="", fmt="", datefmt="", stream=sys.stdout)
LOG_CREATE_ERROR = log_create("fastapi")


class CustomLogger(Logger):

    def __init__(self, config: "Config") -> None:
        super().__init__(config)

        self.access_logger = LOG_CREATE_ACCESS
        self.error_logger = LOG_CREATE_ERROR


def config(hypercorn_config: Config):
    hypercorn_config.logger_class = CustomLogger
