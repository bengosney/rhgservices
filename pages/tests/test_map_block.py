# Django
from django.test import TestCase

# First Party
from pages.blocks import MapBlock


class MapBlockTestCase(TestCase):
    def setUp(self) -> None:
        self.values = {"title": "Test Map", "latitude": 40.712776, "longitude": -74.005974}
        self.hash = "0a2ca8e1d6f9c5c7ad9c5a8996768610"
        return super().setUp()

    def test_get_context(self):
        block = MapBlock()
        context = block.get_context(self.values)
        self.assertIn("self", context)
        self.assertIn("hash", context["self"])
        self.assertEqual(context["self"]["title"], "Test Map")
        self.assertEqual(context["self"]["latitude"], 40.712776)
        self.assertEqual(context["self"]["longitude"], -74.005974)

    def test_hash_generation(self):
        block = MapBlock()
        context1 = block.get_context(self.values)
        self.assertEqual(context1["self"]["hash"], self.hash)
