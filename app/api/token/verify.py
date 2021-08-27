from fastapi import FastAPI
from tortoise.exceptions import DoesNotExist

import services.token as token_service
from exceptions.unauthorized import UnauthorizedException
from helpers.response import EmptyResponse

API_TAGS: list = ["Tokens"]


def register(app: FastAPI):
    @app.api_route(
        tags=API_TAGS,
        path="/api/public/v1/token/verify/{token_value}",
        methods=["GET"]
    )
    async def verify(token_value: str) -> EmptyResponse:
        if not token_value:
            raise UnauthorizedException

        try:
            await token_service.validate(token_value)
        except DoesNotExist:
            raise UnauthorizedException

        return EmptyResponse()
