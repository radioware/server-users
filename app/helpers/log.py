import sys

import aiologger
from aiologger.levels import LogLevel

LOG_FMT_DEFAULT: str = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
LOG_DATEFMT_DEFAULT: str = "[%Y-%m-%dT%H:%M:%S%z]"
LOG_STREAM_DEFAULT = sys.stderr


def log_create(
        name: str,
        fmt: str = LOG_FMT_DEFAULT,
        datefmt: str = LOG_DATEFMT_DEFAULT,
        stream=LOG_STREAM_DEFAULT
) -> aiologger.Logger:
    formatter: aiologger.logger.Formatter = aiologger.logger.Formatter(
        fmt=fmt,
        datefmt=datefmt,
    )

    handler: aiologger.logger.Handler = aiologger.logger.AsyncStreamHandler(
        stream=stream,
        level=LogLevel.DEBUG,
        formatter=formatter
    )

    logger: aiologger.Logger = aiologger.Logger(
        name=name,
        level=LogLevel.DEBUG
    )

    logger.add_handler(handler)

    return logger
