from tortoise.exceptions import DoesNotExist

from exceptions.not_found import NotFoundException
from models.user import User
from utilities.password import PasswordUtility


async def find_by_username_password(email: str, password: str) -> User:
    try:
        db_user: User = await User.get(email=email)
    except DoesNotExist:
        raise NotFoundException

    password_utility = PasswordUtility()
    result = password_utility.verify(db_user.password, password)
    if not result:
        raise NotFoundException

    return db_user
