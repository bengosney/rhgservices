# Standard Library
import tempfile
from os import path

# Django
from django.conf import settings
from django.test import TestCase

# First Party
from localimages.apps import fill_image_with_stock


class LocalImagesTestCase(TestCase):
    def setUp(self) -> None:
        self.tmpDir = tempfile.mkdtemp(dir=settings.MEDIA_ROOT)

    def get_tmp_name(self):
        for i in range(1000):
            filePath = path.join(self.tmpDir, f"no-{i}-img.jpg")
            if not path.exists(filePath):
                return filePath
        else:
            raise Exception("No free file found")

    def test_fill_stock_image(self):
        imgPath = self.get_tmp_name()

        fill_image_with_stock(imgPath)

        self.assertTrue(path.exists(imgPath))
