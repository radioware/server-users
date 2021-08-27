from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    pass


def register(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, e: NotFoundException):
        return JSONResponse(status_code=404, content={})
