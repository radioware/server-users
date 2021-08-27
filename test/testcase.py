import asyncio

import asynctest


class AsyncTestCase(asynctest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        asyncio.get_event_loop().run_until_complete(cls.asyncSetUpClass())

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

        asyncio.get_event_loop().run_until_complete(cls.asyncTearDownClass())

    @classmethod
    async def asyncSetUpClass(cls) -> None:
        pass

    @classmethod
    async def asyncTearDownClass(cls) -> None:
        pass
