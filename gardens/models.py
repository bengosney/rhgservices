# Django
from django.db import models

# Third Party
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class Garden(Page):
    title = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=250, blank=True)

    short_description = models.CharField(max_length=150, blank=True)
    description = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

    content_panels = Page.content_panels + [FieldPanel("body", classname="full")]
