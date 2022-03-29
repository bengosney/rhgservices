# Wagtail
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

# First Party
from projects.models import Project


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
