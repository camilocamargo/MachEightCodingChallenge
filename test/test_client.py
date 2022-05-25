import unittest
from data.client import Client
from settings import DATASOURCE_URL


class TestClient(unittest.TestCase):
    def test_get_200(self):
        client = Client(DATASOURCE_URL)
        response = client.get()
        self.assertEqual(response.status_code, 200)

    def test_get_404(self):
        client = Client('https://mach-eight.uc.r.appspot.com/badendpoint')
        response = client.get()
        self.assertEqual(response.status_code, 404)

    def test_content_is_not_none(self):
        client = Client(DATASOURCE_URL)
        response = client.get()
        self.assertIsNotNone(response.content)

    def test_content_is_json(self):
        client = Client(DATASOURCE_URL)
        response = client.get()
        self.assertEqual(response.headers.get('content-type'), 'application/json')
