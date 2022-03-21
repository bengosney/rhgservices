# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class Garden(Page):
    sub_title = models.CharField(max_length=250, blank=True)

    short_description = models.CharField(max_length=150, blank=True)
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

    content_panels = Page.content_panels + [FieldPanel("short_description"), StreamFieldPanel("body")]
