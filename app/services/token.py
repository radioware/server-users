import datetime

import utilities.token as token_utility
from exceptions.invalid_data import InvalidDataException
from exceptions.unauthorized import UnauthorizedException
from models.token import Token
from models.user import User


async def generate_token(user: User) -> Token:
    token_value: str = token_utility.generate_token_value()

    token: Token = Token()
    token.token = token_value
    token.user = user
    token.validity_start = datetime.datetime.now()
    token.validity_duration = datetime.timedelta(hours=24)
    await token.save()

    return token


async def validate(token_value: str) -> Token:
    if not token_value:
        raise InvalidDataException

    token: Token = await Token.get(token=token_value)
    if not token_utility.validate_expiration(token.validity_start, token.validity_duration):
        raise UnauthorizedException

    return token
