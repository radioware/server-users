import os
import signal
import subprocess
import sys
import unittest


class AppTestCase(unittest.TestCase):
    _process: subprocess.Popen

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

        self._process: subprocess.Popen

    def setUp(self) -> None:
        super().setUp()

        env: dict = {}

        cwd: str = os.path.abspath("../app")
        args: list[str] = [sys.executable, "main.py"]
        self._process = subprocess.Popen(
            cwd=cwd,
            args=args,
            env=env
        )

    def tearDown(self) -> None:
        self._process.send_signal(signal.SIGINT)

        super().tearDown()
