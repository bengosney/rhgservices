# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

# Third Party
from modelcluster.fields import ParentalKey

# Locals
from .blocks import CallOutBlock, FlexBlock, FlexStreamBlock, FormBlock, InfoPodBlock, MapBlock, ProjectsBlock


class HomePage(Page):
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", FlexBlock(InfoPodBlock())),
            ("Paragraph", blocks.RichTextBlock()),
            ("Projects", ProjectsBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("body"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class InfoPage(Page):
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", blocks.ListBlock(InfoPodBlock())),
            ("Paragraph", blocks.RichTextBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]


class FormPage(AbstractEmailForm):
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", blocks.ListBlock(InfoPodBlock())),
            ("Paragraph", blocks.RichTextBlock()),
            ("Form", FormBlock()),
            ("Map", MapBlock()),
            (
                "Row",
                FlexStreamBlock(
                    [
                        ("Form", FormBlock()),
                        ("Map", MapBlock()),
                    ]
                ),
            ),
        ],
        blank=True,
    )
    thank_you_text = RichTextField(blank=True)
    submit_text = models.CharField(max_length=255, default="Submit")

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        StreamFieldPanel("body"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel(
            [
                FieldPanel("submit_text"),
                FieldPanel("thank_you_text"),
            ],
            "Submit",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]
