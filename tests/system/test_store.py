import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test")

                self.assertEqual(201, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name("test"))
                self.assertDictEqual({"id": 1, "name": "test", "items": []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test")
                response = client.post("/store/test")

                self.assertEqual(400, response.status_code)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                response = client.delete("/store/test")

                self.assertEqual(200, response.status_code)
                self.assertIsNone(StoreModel.find_by_name("test"))
                self.assertDictEqual({"message": "Store deleted"}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                response = client.get("/store/test")

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"id": 1, "name": "test", "items": []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test")

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({"message": "Store not found"}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test item1", 19.99, 1).save_to_db()
                ItemModel("test item2", 19.99, 1).save_to_db()

                expected = {
                    "id": 1,
                    "name": "test",
                    "items": [
                        {"name": "test item1", "price": 19.99},
                        {"name": "test item2", "price": 19.99},
                    ],
                }

                response = client.get("/store/test")

                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                StoreModel("test2").save_to_db()
                expected = {
                    "stores": [
                        {"id": 1, "name": "test", "items": []},
                        {"id": 2, "name": "test2", "items": []}
                    ],
                }
                response = client.get("/stores")

                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test item1", 19.99, 1).save_to_db()
                expected = {
                    "stores": [
                        {
                            "id": 1,
                            "name": "test",
                            "items": [
                                {"name": "test item1", "price": 19.99},
                            ]
                        }
                    ]
                }

                response = client.get("/stores")

                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, json.loads(response.data))
