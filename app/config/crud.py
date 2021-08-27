import inspect
import os

from fastapi import FastAPI
from fastapi_crudrouter import TortoiseCRUDRouter
from tortoise import Model

import models
from helpers.log import log_create

API_CRUD_PREFIX: str = os.environ.get("API_CRUD_PREFIX", "/api/crud")

_logger = log_create(__name__)


def is_model(obj):
    return isinstance(obj, type) and issubclass(obj, Model)


async def startup(app: FastAPI) -> None:
    await _logger.info("Configuring CRUD")

    modules: list = [x[1] for x in inspect.getmembers(models, inspect.ismodule)]
    await _logger.debug(f"Detected {len(modules)} modules")

    model_classes: list = []

    for module in modules:
        module_classes = [x[1] for x in inspect.getmembers(module, is_model)]
        await _logger.debug(f"Detected {len(module_classes)} classes in {module.__name__}")
        model_classes.extend(module_classes)

    model_classes = list(set(model_classes))
    await _logger.debug(f"We have {len(model_classes)} classes to register for CRUD")

    for model_class in list(set(model_classes)):
        router: TortoiseCRUDRouter = model_class.get_router()
        app.include_router(router, prefix=API_CRUD_PREFIX)
