# Standard Library
import os
from pathlib import Path
from random import randint

# Django
from django.apps import AppConfig
from django.conf import settings

# Third Party
import requests
import wrapt


def fill_image_with_stock(path):
    Path(path).parent.mkdir(exist_ok=True)
    baseURL = f"https://picsum.photos/{randint(6, 12) * 100}/{randint(6, 12) * 100}"
    img_data = requests.get(baseURL)
    with open(path, "wb") as handler:
        handler.write(img_data.content)


class LocalImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "localimages"
    path = os.path.join(settings.BASE_DIR, "localimages")

    def ready(self) -> None:
        # Wagtail
        from wagtail.images.models import AbstractImage, SourceImageIOError

        @wrapt.patch_function_wrapper(AbstractImage, "generate_rendition_file")
        def fake_image(wrapped, instance, args, kwargs):
            try:
                return wrapped(*args, **kwargs)
            except SourceImageIOError:
                print("---=== (( *** )) ===---")
                fill_image_with_stock(instance.file.path)

                return wrapped(*args, **kwargs)

        return super().ready()
