# Django
from django.db import models

# Wagtail
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page

# Third Party
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class ProjectListPage(Page):
    show_in_menus_default = True

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

    panels = [FieldPanel("image"), FieldPanel("caption")]


class Project(Page):
    show_in_menus_default = True

    sub_title = models.CharField(max_length=250, blank=True)
    tags = ClusterTaggableManager(through=ProjectTag, blank=True)
    short_description = models.CharField(max_length=150, blank=True)
    body = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def banner_image(self):
        if self.hero_image:
            return self.hero_image

        return img.image if (img := self.images.first()) else None

    content_panels = [
        MultiFieldPanel(
            Page.content_panels
            + [
                FieldPanel("hero_image"),
                FieldPanel("sub_title"),
                FieldPanel("tags"),
            ],
            heading="Project Information",
        ),
        InlinePanel("images", label="Images"),
        FieldPanel("short_description"),
        FieldPanel("body"),
    ]
