import inspect
import os

from fastapi import FastAPI
from tortoise import Tortoise

import models
from helpers.log import log_create

DB_URL = "postgres://{username}:{password}@{host}:{port}/{database}".format(
    host=os.environ.get("DB_HOST", "127.0.0.1"),
    port=os.environ.get("DB_PORT", 5432),
    username=os.environ.get("DB_USER", "gufo"),
    password=os.environ.get("DB_PASSWORD", "gufo"),
    database=os.environ.get("DB_NAME", "gufo")
)

GENERATE_SCHEMA: bool = bool(os.environ.get("DB_GENERATE_SCHEMA", "False").lower() == "true")

_logger = log_create(__name__)


def generate_modules_list() -> list[str]:
    return [x[1].__name__ for x in inspect.getmembers(models, inspect.ismodule)]


async def startup(app: FastAPI) -> None:  # pylint: disable=W0612
    await _logger.info("Configuring Tortoise-ORM")

    models_module_names: list[str] = generate_modules_list()
    await _logger.debug(f"Found {len(models_module_names)} modules to init")

    modules: dict = {
        "users": models_module_names
    }

    await _logger.debug("Initializing Tortoise")
    await Tortoise.init(db_url=DB_URL, modules=modules)
    await _logger.debug("Tortoise-ORM started.")

    if GENERATE_SCHEMA:
        await _logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()
        await _logger.debug("Schema generated")


async def shutdown() -> None:
    await _logger.info("Shutting down Tortoise-ORM")
    await Tortoise.close_connections()
    await _logger.debug("Tortoise-ORM shutdown complete")
