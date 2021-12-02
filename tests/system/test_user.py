import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertDictEqual({"message": "A user was created successfully"}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "test", "password": "1234"})
                auth_response = client.post("/auth",
                                           data=json.dumps({"username": "test", "password": "1234"}),
                                           headers={"Content-type": "application/json"})

                self.assertIn("access_token", json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={"username": "test", "password": "1234"})
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({"message": "A user with such name is already exists"}, json.loads(response.data))
