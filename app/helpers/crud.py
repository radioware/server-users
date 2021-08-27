from typing import Type, Optional

import inflect
from fastapi_crudrouter import TortoiseCRUDRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class AbstractCrudModel:

    @classmethod
    def get_schema(cls) -> Optional[Type[BaseModel]]:
        return pydantic_model_creator(cls=cls, name=f"{cls.__name__}Schema")

    @classmethod
    def get_schema_create(cls) -> Optional[Type[BaseModel]]:
        return pydantic_model_creator(cls=cls, name=f"{cls.__name__}SchemaCreate", exclude_readonly=True)

    @classmethod
    def get_schema_update(cls) -> Optional[Type[BaseModel]]:
        return cls.get_schema_create()

    @classmethod
    def get_router(cls) -> TortoiseCRUDRouter:
        model_class_name: str = cls.__name__.lower()
        inflect_engine: inflect.engine = inflect.engine()
        api_prefix: str = inflect_engine.plural_noun(model_class_name)

        tags: list = [f"CRUD {api_prefix.capitalize()}"]

        schema = cls.get_schema()
        create_schema = cls.get_schema_create()
        update_schema = cls.get_schema_update()

        return TortoiseCRUDRouter(
            db_model=cls,
            prefix=api_prefix,
            tags=tags,
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema
        )
