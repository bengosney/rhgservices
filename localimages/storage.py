import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

import requests
from PIL import Image


class DevImageStorage(FileSystemStorage):
    """
    Storage that fabricates an image if the file does not exist.
    Allows Wagtail to generate renditions normally.
    """

    def _generate_placeholder(self):
        url = "https://picsum.photos/1600/900"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return ContentFile(response.content)
        except Exception:
            img = Image.new("RGB", (1600, 900), (163, 163, 163))

            buf = BytesIO()
            img.save(buf, format="JPEG")

            return ContentFile(buf.getvalue())

    def open(self, name, mode="rb"):
        path = os.path.join(self.location, name)

        if not os.path.exists(path):
            return self._generate_placeholder()

        return super().open(name, mode)
