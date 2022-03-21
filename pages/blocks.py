# Wagtail
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class FlexBlock(blocks.ListBlock):
    class Meta:
        template = "pages/blocks/flex_block.html"


class InfoPodBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock()
    paragraph = blocks.CharBlock(required=False, help_text="Optional")

    class Meta:
        template = "pages/blocks/infopod.html"


class CallOutBlock(blocks.StructBlock):
    headline = blocks.CharBlock()
    subline = blocks.CharBlock()

    class Meta:
        template = "pages/blocks/callout.html"
