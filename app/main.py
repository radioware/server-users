import dotenv

dotenv.load_dotenv()

import asyncio
import signal

from fastapi import FastAPI
from hypercorn import Config
from hypercorn.asyncio import serve

import config

app: FastAPI = FastAPI(title="Users Microservice")


async def app_init() -> None:
    await config.crud.startup(app)
    await config.api.startup(app)


async def db_startup() -> None:
    await config.tortoise.startup(app)


async def db_shutdown() -> None:
    await config.tortoise.shutdown()


hypercorn_config = Config()
config.hypercorn.config(hypercorn_config)
config.logger.config(hypercorn_config)

loop = asyncio.get_event_loop()
shutdown_event = asyncio.Event()


def signal_handler() -> None:
    shutdown_event.set()


def main():
    loop.add_signal_handler(signal.SIGINT, signal_handler)
    loop.add_signal_handler(signal.SIGHUP, signal_handler)
    loop.add_signal_handler(signal.SIGTERM, signal_handler)

    loop.run_until_complete(db_startup())
    loop.run_until_complete(app_init())
    loop.run_until_complete(serve(app, hypercorn_config, shutdown_trigger=shutdown_event.wait))
    loop.run_until_complete(db_shutdown())


if __name__ == "__main__":
    main()
