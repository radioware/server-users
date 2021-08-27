import datetime
import uuid

import pytz


def generate_token_value() -> str:
    return str(uuid.uuid4())


def validate_expiration(validity_start: datetime.datetime, validity_duration: datetime.timedelta) -> bool:
    if not validity_start:
        return False

    if not validity_duration:
        return False

    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    return bool(validity_start + validity_duration >= now)
