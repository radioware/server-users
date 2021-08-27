import datetime
import uuid
from typing import Optional, Iterable

from tortoise import models, fields, BaseDBAsyncClient

from helpers.crud import AbstractCrudModel
from models.role import Role
from utilities.password import PasswordUtility


class User(models.Model, AbstractCrudModel):
    id = fields.UUIDField(
        description="Primary Key",
        pk=True,
        default=lambda: uuid.uuid4()
    )

    email = fields.CharField(
        description="User e-mail address",
        max_length=255,
        unique=True,
        index=True
    )

    password = fields.CharField(
        description="User Password",
        max_length=255
    )

    ts_create = fields.DatetimeField(
        description="Timestamp of creation",
        default=lambda: datetime.datetime.utcnow()
    )

    roles: fields.ManyToManyRelation[Role] = fields.ManyToManyField(
        model_name="users.Role",
        related_name="users"
    )

    tokens = fields.ReverseRelation["users.Token"]

    def __str__(self):
        return self.email

    async def save(
            self,
            using_db: Optional[BaseDBAsyncClient] = None,
            update_fields: Optional[Iterable[str]] = None,
            force_create: bool = False,
            force_update: bool = False
    ) -> None:
        if self.password and not self.password.startswith("$argon2"):
            password_utility = PasswordUtility()
            self.password = password_utility.hash(self.password)

        return await super().save(using_db, update_fields, force_create, force_update)
