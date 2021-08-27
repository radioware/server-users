import datetime
import uuid

from pydantic import BaseModel


class CustomModel(BaseModel):
    class Config:
        orm_mode = True

        json_encoders = {
            datetime.datetime: lambda x: x.timestamp(),
            datetime.timedelta: lambda x: x.total_seconds(),
            uuid.UUID: lambda x: str(x)
        }
