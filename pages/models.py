# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

# Locals
from .blocks import CallOutBlock, FlexBlock, InfoPodBlock


class HomePage(Page):
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", FlexBlock(InfoPodBlock())),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("body"),
    ]


class InfoPage(Page):
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", blocks.ListBlock(InfoPodBlock())),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
