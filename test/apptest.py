import os
import sys

from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from testcase import AsyncTestCase


class AppTestCase(AsyncTestCase):
    _client: TestClient

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls._add_app_path()

        from config.tortoise import generate_modules_list
        initializer(
            app_label="users",
            modules=generate_modules_list()
        )

        import main
        cls._client = TestClient(main.app)

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @classmethod
    async def asyncSetUpClass(cls) -> None:
        cls._add_app_path()

        import main
        await main.app_init()

    def tearDown(self) -> None:
        super().tearDown()

        finalizer()

    @classmethod
    def _add_app_path(cls) -> None:
        app_path: str = os.path.abspath("../app")
        if app_path not in sys.path:
            sys.path.append(app_path)
