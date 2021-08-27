from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class InvalidDataException(Exception):
    pass


def register(app: FastAPI):
    @app.exception_handler(InvalidDataException)
    async def not_found_exception_handler(request: Request, e: InvalidDataException):
        return JSONResponse(status_code=422, content={})
