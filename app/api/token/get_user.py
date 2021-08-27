from fastapi import FastAPI
from tortoise.exceptions import DoesNotExist

import services.token as token_service
from exceptions.unauthorized import UnauthorizedException
from models.token import Token
from models.user import User

API_TAGS: list = ["Tokens"]


def register(app: FastAPI):
    @app.api_route(
        tags=API_TAGS,
        path="/api/public/v1/token/get-user/{token_value}",
        methods=["GET"],
    )
    async def get_user(token_value: str) -> User:
        if not token_value:
            raise UnauthorizedException

        try:
            token: Token = await token_service.validate(token_value)
        except DoesNotExist:
            raise UnauthorizedException

        user: User = await token.user

        return user
