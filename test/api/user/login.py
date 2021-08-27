import requests

from apptest import AppTestCase

TEST_USER_EMAIL: str = "user@domain.tld"
TEST_USER_PASSWORD: str = "password"

TEST_USER2_EMAIL: str = "user2@domain.tld"
TEST_USER2_PASSWORD: str = "password2"


class LoginTest(AppTestCase):
    def test_create_user(self):
        request_body: dict = {
            "username": TEST_USER2_EMAIL,
            "password": TEST_USER2_PASSWORD,
        }

        response = requests.post(url="http://127.0.0.1:8090/api/crud/users", json=request_body)

        self.assertEqual(response.status_code, 201)
