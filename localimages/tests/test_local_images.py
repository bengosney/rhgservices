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
        self.tmpDir = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)

    def get_tmp_name(self):
        for i in range(1000):
            filePath = path.join(self.tmpDir, f"no-{i}-img.jpg")
            if not path.exists(filePath):
                return filePath
        raise Exception("No free file found")

    @skipIf(cant_mkdtemp(), "Can't make a temp file")
    def test_fill_stock_image(self):
        imgPath = self.get_tmp_name()

        fill_image_with_stock(imgPath)

        self.assertTrue(path.exists(imgPath))
