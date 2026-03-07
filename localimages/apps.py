from django.apps import AppConfig
from django.conf import settings


class LocalImagesConfig(AppConfig):
    name = "localimages"

    def ready(self):
        if not settings.DEBUG:
            return

        from wagtail.images.models import Image  # noqa: PLC0415

        from localimages.storage import DevImageStorage  # noqa: PLC0415

        Image._meta.get_field("file").storage = DevImageStorage()
