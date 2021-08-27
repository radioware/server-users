import datetime

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from tortoise import Tortoise

import services.token as token_service
import services.user as user_service
from helpers.model import CustomModel
from models.token import Token
from models.user import User

API_TAGS: list = ["Users"]


class RequestModel(BaseModel):
    email: EmailStr
    password: str


class ResponseModel(CustomModel):
    token: str
    validity_start: datetime.datetime
    validity_duration: datetime.timedelta


def register(app: FastAPI):
    @app.api_route(
        tags=API_TAGS,
        path="/api/public/v1/user/login",
        methods=["POST"]
    )
    async def login(request_body: RequestModel) -> ResponseModel:
        conn = Tortoise.get_connection("default")
        print(conn)

        user: User = await user_service.find_by_username_password(request_body.email, request_body.password)
        token: Token = await token_service.generate_token(user)
        await token.fetch_related()
        return ResponseModel(
            token=token.token,
            validity_start=token.validity_start,
            validity_duration=token.validity_duration
        )
