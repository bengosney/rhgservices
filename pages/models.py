# Django
from django.db import models

# Wagtail
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

# Third Party
from modelcluster.fields import ParentalKey

# Locals
from .blocks import CallOutBlock, FlexBlock, FlexStreamBlock, FormBlock, InfoPodBlock, MapBlock, ProjectsBlock


@register_setting
class SiteSettings(BaseSetting):
    phone_number = models.CharField(max_length=255, help_text="Phone number to show in the footer", default="")
    facebook = models.URLField(help_text="Your Facebook page URL", default="")
    instagram = models.CharField(max_length=255, help_text="Your Instagram username, without the @", default="")
    checkatrade = models.URLField(max_length=255, help_text="Your checkatrade link", default="")


class HomePage(Page):
    show_in_menus_default = True

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False, on_delete=models.SET_NULL, related_name="+")
    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", FlexBlock(InfoPodBlock())),
            ("Paragraph", blocks.RichTextBlock()),
            ("Projects", ProjectsBlock()),
        ],
        use_json_field=True,
    )

    parent_page_types = ["wagtailcore.Page"]

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("body"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


class InfoPage(Page):
    show_in_menus_default = True

    body = StreamField(
        [
            ("Callout", CallOutBlock()),
            ("InfoPod", blocks.ListBlock(InfoPodBlock())),
            ("Paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class FormPage(AbstractEmailForm):
    show_in_menus_default = True

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
        use_json_field=True,
    )
    thank_you_text = RichTextField(blank=True)
    submit_text = models.CharField(max_length=255, default="Submit")

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("body"),
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
