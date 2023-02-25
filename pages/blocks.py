# Standard Library
from hashlib import md5

# Wagtail
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# First Party
from projects.models import Project


class FlexStreamBlock(blocks.StreamBlock):
    class Meta:
        template = "pages/blocks/flex_stream.html"


class FlexBlock(blocks.ListBlock):
    class Meta:
        template = "pages/blocks/flex_block.html"


class ProjectsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, max_length=255)
    body = blocks.RichTextBlock(required=False)
    projects = blocks.ListBlock(blocks.PageChooserBlock(target_model=Project))

    class Meta:
        template = "pages/blocks/projects.html"


class InfoPodBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    paragraph = blocks.CharBlock(required=False, help_text="Optional")
    page = blocks.PageChooserBlock(required=False)

    class Meta:
        template = "pages/blocks/infopod.html"


class CallOutBlock(blocks.StructBlock):
    headline = blocks.CharBlock()
    subline = blocks.CharBlock()

    class Meta:
        template = "pages/blocks/callout.html"


class FormBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)

    class Meta:
        template = "pages/blocks/form.html"
        icon = "form"


class MapBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    latitude = blocks.FloatBlock()
    longitude = blocks.FloatBlock()

    class Meta:
        template = "pages/blocks/map.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context_string = "-".join([f"{c}:{context['self'][c]}" for c in context["self"]])
        context["self"]["hash"] = md5(context_string.encode("utf-8")).hexdigest()

        return context
