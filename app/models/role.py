import uuid

from tortoise import models, fields

from helpers.crud import AbstractCrudModel


class Role(models.Model, AbstractCrudModel):
    id = fields.UUIDField(
        description="Primary Key",
        pk=True,
        default=lambda: uuid.uuid4()
    )

    name = fields.CharField(
        description="User e-mail address",
        max_length=255,
        unique=True,
        index=True
    )

    users: fields.ManyToManyRelation["User"]

    def __str__(self):
        return self.name

    class Meta:
        table = "role"
        table_description = "Roles"
