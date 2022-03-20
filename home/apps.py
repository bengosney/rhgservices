# Django
from django.apps import AppConfig

# Third Party
import rustface.willow
from willow.registry import registry


class HomeConfig(AppConfig):
    name = "home"

    def ready(self) -> None:
        registry.register_plugin(rustface.willow)

        return super().ready()
