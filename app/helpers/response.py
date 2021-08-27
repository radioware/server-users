from starlette.background import BackgroundTask
from starlette.responses import Response


class EmptyResponse(Response):
    def __init__(
            self,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None
    ) -> None:
        super().__init__("", 204, headers, media_type, background)
