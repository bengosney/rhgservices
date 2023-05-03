# Django
from django.db import models

# Wagtail
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class Robots(BaseSiteSetting):
    contents = models.TextField(blank=True)
