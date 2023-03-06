# Standard Library
from pathlib import Path
from random import randint

# Django
from django.apps import AppConfig

# Third Party
import requests
import wrapt


class LocalimagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "localimages"

    def ready(self) -> None:
        # Wagtail
        from wagtail.images.models import AbstractImage, SourceImageIOError

        @wrapt.patch_function_wrapper(AbstractImage, "generate_rendition_file")
        def fake_image(wrapped, instance, args, kwargs):
            try:
                return wrapped(*args, **kwargs)
            except SourceImageIOError:
                Path(instance.file.path).parent.mkdir(exist_ok=True)
                baseURL = f"https://picsum.photos/{randint(6, 12) * 100}/{randint(6, 12) * 100}"
                img_data = requests.get(baseURL)
                with open(instance.file.path, "wb") as handler:
                    handler.write(img_data.content)

                return wrapped(*args, **kwargs)

        return super().ready()
