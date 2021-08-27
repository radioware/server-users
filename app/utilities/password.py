from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError

from helpers.singleton import Singleton


class PasswordUtility(metaclass=Singleton):

    def __init__(self):
        self._ph = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._ph.hash(password)

    def verify(self, hashed: str, password: str) -> bool:
        try:
            return self._ph.verify(hash=hashed, password=password)
        except VerificationError:
            return False
        except InvalidHash:
            return False

    def rehash(self, hashed: str, password: str) -> str:
        if self._ph.check_needs_rehash(hash=hashed):
            return self.hash(password=password)
        return ""
