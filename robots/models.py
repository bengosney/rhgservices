# Django
from django.db import models

# Wagtail
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class Robots(BaseSetting):
    contents = models.TextField(blank=True)
