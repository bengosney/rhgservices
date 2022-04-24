# Django
from django.test import TestCase

# Locals
from .templatetags.picture_tags import get_media_query


class PictureTagTests(TestCase):
    def test_spec_parse(self):
        class fakeImage:
            width = 100

        specs = (
            ("max-1000x500", "max-width: 100px"),
            ("height-480", "max-width: 100px"),
            ("scale-50", "max-width: 100px"),
            ("original", "max-width: 100px"),
            ("width-640", "max-width: 640px"),
            ("fill-200x200", "max-width: 200px"),
            ("min-500x200", "min-width: 500px"),
        )

        for spec, expected in specs:
            self.assertEqual(get_media_query(spec, fakeImage()), expected)
