import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("test", "1234").save_to_db()
                auth_response = client.post("/auth",
                                            data=json.dumps({"username": "test", "password": "1234"}),
                                            headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_response.data)["access_token"]
                self.access_token = f"JWT {auth_token}"

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/test")
                self.assertEqual(401, response.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()
                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()
                response = client.delete("/item/test")
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"message": "Item deleted"}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                response = client.post("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(201, response.status_code)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.post("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(400, response.status_code)
                self.assertDictEqual({"message": "An item with name 'test' already exists."},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                response = client.put("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(19.99, ItemModel.find_by_name("test").price)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_put_item_update(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 29.99, 1).save_to_db()
                self.assertEqual(29.99, ItemModel.find_by_name("test").price)

                response = client.put("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(19.99, ItemModel.find_by_name("test").price)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 29.99, 1).save_to_db()
                expected = {
                    "items": [
                        {"name": "test", "price": 29.99},
                    ]
                }

                response = client.get("/items")
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

