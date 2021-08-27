import os

from hypercorn import Config


def config(hypercorn_config: Config):
    hypercorn_config.access_log_format = "%(h)s %(l)s %(l)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\""
    hypercorn_config.use_reloader = bool(os.environ.get("ENABLE_RELOADER", "False").lower() == "true")
    hypercorn_config.bind = [x.strip() for x in os.environ.get("BIND_ADDRESSES", "[::]:8080").split(",") if x.strip()]
