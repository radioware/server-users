from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnauthorizedException(Exception):
    pass


def register(app: FastAPI):
    @app.exception_handler(UnauthorizedException)
    async def not_found_exception_handler(request: Request, e: UnauthorizedException):
        return JSONResponse(status_code=401, content={})
