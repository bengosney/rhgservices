# Third Party
from icecream import ic
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

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        ic(context)
        print(context)
        print("-----")
        return context


class CallOutBlock(blocks.StructBlock):
    headline = blocks.CharBlock()
    subline = blocks.CharBlock()

    class Meta:
        template = "pages/blocks/callout.html"
