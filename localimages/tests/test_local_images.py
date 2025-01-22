# Standard Library
import tempfile
from os import path
from unittest import skipIf

# Django
from django.conf import settings
from django.test import TestCase

# First Party
from localimages.apps import fill_image_with_stock


def cant_mkdtemp():
    try:
        tempfile.mkdtemp(dir=settings.MEDIA_ROOT)
        return False
    except Exception:
        return True


class LocalImagesTestCase(TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)

    def get_tmp_name(self):
        for i in range(1000):
            file_path = path.join(self.tmp_dir, f"no-{i}-img.jpg")
            if not path.exists(file_path):
                return file_path
        raise Exception("No free file found")

    @skipIf(cant_mkdtemp(), "Can't make a temp file")
    def test_fill_stock_image(self):
        img_path = self.get_tmp_name()

        fill_image_with_stock(img_path)

        self.assertTrue(path.exists(img_path))
