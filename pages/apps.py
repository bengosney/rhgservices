# Standard Library
import contextlib

# Django
from django.apps import AppConfig

# Third Party
import rustface.willow
from willow.registry import registry


def patch_images():
    # Wagtail
    from wagtail.images.models import AbstractImage, SourceImageIOError

    # Third Party
    import requests
    import wrapt

    @wrapt.patch_function_wrapper(AbstractImage, "generate_rendition_file")
    def fake_image(wrapped, instance, args, kwargs):
        try:
            return wrapped(*args, **kwargs)
        except SourceImageIOError:
            baseURL = "https://picsum.photos/800/600"
            img_data = requests.get(baseURL)
            with open(instance.file.path, "wb") as handler:
                handler.write(img_data.content)

            return wrapped(*args, **kwargs)


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"

    def ready(self) -> None:
        registry.register_plugin(rustface.willow)
        with contextlib.suppress(ModuleNotFoundError):
            patch_images()
        return super().ready()
