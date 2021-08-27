import datetime
import uuid
from typing import Optional, Type

from pydantic import BaseModel
from tortoise import models, fields

from helpers.crud import AbstractCrudModel
from helpers.model import CustomModel
from models.user import User


class Token(models.Model, AbstractCrudModel):
    id = fields.UUIDField(
        description="Primary Key",
        pk=True,
        default=lambda: uuid.uuid4()
    )

    token = fields.CharField(
        description="Token value",
        max_length=255,
        unique=True,
        index=True
    )

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        description="Related User ID",
        model_name="users.User",
        null=True,
        on_delete=fields.SET_NULL,
        index=True
    )

    validity_start = fields.DatetimeField(
        description="Timestamp of start of validity of the Token",
        default=lambda: datetime.datetime.utcnow(),
        index=True
    )

    validity_duration = fields.TimeDeltaField(
        description="Duration in seconds of the Token"
    )

    def __str__(self):
        return self.token

    # class Meta:
    #     table = "token"
    #     table_description = "Users Tokens"
    #
    # class TokenSchema(CustomModel):
    #     id: uuid.UUID
    #     user_id: int
    #     validity_start: datetime.datetime
    #     validity_duration: datetime.timedelta
    #
    # class TokenSchemaCreate(CustomModel):
    #     user_id: int
    #     validity_duration: Optional[int]
    #
    # class TokenSchemaUpdate(CustomModel):
    #     validity_duration: Optional[int]
    #
    # @classmethod
    # def get_schema(cls) -> Optional[Type[BaseModel]]:
    #     return cls.TokenSchema
    #
    # @classmethod
    # def get_schema_create(cls) -> Optional[Type[BaseModel]]:
    #     return cls.TokenSchemaCreate
    #
    # @classmethod
    # def get_schema_update(cls) -> Optional[Type[BaseModel]]:
    #     return cls.TokenSchemaUpdate
