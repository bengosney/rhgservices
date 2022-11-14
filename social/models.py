# Django
from django.db import models

# Wagtail
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class Social(BaseSetting):
    description = models.CharField(max_length=255)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    json_ld = models.TextField(blank=True)
