# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel

# Third Party
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class ProjectListPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        projectpages = self.get_children().live().type(Project)
        context["projectpages"] = projectpages
        return context


class ProjectTag(TaggedItemBase):
    content_object = ParentalKey("Project", related_name="tagged_items", on_delete=models.CASCADE)


class ProjectImage(Orderable):
    project = ParentalKey("Project", related_name="images", on_delete=models.CASCADE)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [ImageChooserPanel("image"), FieldPanel("caption")]


class Project(Page):
    sub_title = models.CharField(max_length=250, blank=True)
    tags = ClusterTaggableManager(through=ProjectTag, blank=True)
    short_description = models.CharField(max_length=150, blank=True)
    body = RichTextField(blank=True)

    def banner_image(self):
        return img.image if (img := self.images.first()) else None

    content_panels = [
        MultiFieldPanel(
            Page.content_panels
            + [
                FieldPanel("sub_title"),
                FieldPanel("tags"),
            ],
            heading="Project Information",
        ),
        InlinePanel("images", label="Images"),
        FieldPanel("short_description"),
        FieldPanel("body"),
    ]
