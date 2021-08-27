import inspect

from fastapi import FastAPI

import api
import exceptions
from helpers.log import log_create

_logger = log_create(__name__)


def discover(main_module, methods_list: list = None):
    if methods_list is None:
        methods_list = []

    modules: list = [
        x[1]
        for x in inspect.getmembers(main_module, inspect.ismodule) if
        x[1].__name__.startswith(main_module.__name__)
    ]
    for module in modules:
        discover(module, methods_list)

    functions: list = [
        x[1]
        for x in inspect.getmembers(main_module, inspect.isfunction)
        if x[0] == "register"
    ]
    for func in functions:
        methods_list.append(func)

    return methods_list


async def startup(app: FastAPI) -> None:
    await _logger.info("Configuring APIs")

    funcs: list = discover(api)
    await _logger.debug(f"Found {len(funcs)} APIs to register")
    for func in funcs:
        func(app)

    funcs: list = discover(exceptions)
    await _logger.debug(f"Found {len(funcs)} Exceptions to register")
    for func in funcs:
        func(app)
