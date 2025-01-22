# Third Party
import rustface.willow
from django.apps import AppConfig
from willow.registry import registry


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"

    def ready(self) -> None:
        registry.register_plugin(rustface.willow)
        return super().ready()
