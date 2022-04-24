# Standard Library
import os
import re
from io import BytesIO

# Django
from django import template
from django.core.files import File
from django.utils.safestring import mark_safe

# Wagtail
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import Filter, Rendition

try:
    # Third Party
    import willowavif  # noqa
except ImportError:
    pass


register = template.Library()


def get_media_query(spec, image):
    mediaquery = ""
    r = re.compile(r"^(?P<op>\w+)((-(?P<size>\d+))(x(\d+))?)?$")
    match = r.match(spec)
    if match:
        groups = match.groupdict()
        if groups["op"] in ["fill", "width"]:
            mediaquery = f'max-width: {groups["size"]}px'
        elif groups["op"] in ["max", "height", "scale", "original"]:
            mediaquery = f"max-width: {image.width}px"
        elif groups["op"] in ["min"]:
            mediaquery = f'min-width: {groups["size"]}px'

    return mediaquery


def get_avif_rendition(image, imageRendition, filter_spec):
    avifSpec = "|".join([filter_spec, "format-avif"])
    try:
        avifRendition = image.get_rendition(avifSpec)
    except InvalidFilterSpecError:
        cache_key = ""
        try:
            avifRendition = image.renditions.get(
                filter_spec=avifSpec,
                focal_point_key=cache_key,
            )
        except Rendition.DoesNotExist:
            with imageRendition.get_willow_image() as willow:
                avifImage = willow.save_as_avif(BytesIO())

            input_filename_without_extension, _ = os.path.splitext(image.filename)
            output_extension = avifSpec.replace("|", ".") + ".avif"
            output_filename_without_extension = input_filename_without_extension[: (59 - len(output_extension))]
            output_filename = output_filename_without_extension + "." + output_extension

            avifRendition, _ = image.renditions.get_or_create(
                filter_spec=avifSpec, focal_point_key=cache_key, defaults={"file": File(avifImage.f, name=output_filename)}
            )
    return avifRendition


def get_renditions(image, filter_spec):
    """Get a list of renditions that match the filter specification."""
    if not filter_spec:
        return []

    try:
        _ = Filter(spec=filter_spec)
    except InvalidFilterSpecError:
        return []

    webpRendition = image.get_rendition("|".join([filter_spec, "format-webp"]))
    jpegRendition = image.get_rendition("|".join([filter_spec, "format-jpeg"]))
    pngRendition = image.get_rendition("|".join([filter_spec, "format-png"]))

    renditions = [
        webpRendition,
        jpegRendition,
        pngRendition,
    ]

    try:
        renditions.append(get_avif_rendition(image, webpRendition, filter_spec))
    except AttributeError:
        pass

    renditions.sort(key=lambda r: r.file.size)

    return renditions


@register.tag()
def picture(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])
    filter_specs = bits[1:]

    return PictureNode(image_expr, filter_specs)


class PictureNode(template.Node):
    def __init__(self, image, specs):
        self.image = image
        self.specs = specs
        super().__init__()

    def render(self, context):
        image = self.image.resolve(context)
        if image is None:
            return ""

        baseSpec = self.specs[0]
        sizedSpecs = self.specs[1:]
        base = None

        srcsets = []

        def get_type(ext):
            _type = "jpeg" if ext == "jpg" else ext.replace(".", "")
            return f"image/{_type}"

        for spec in sizedSpecs:
            renditions = get_renditions(image, spec)
            for rendition in renditions:
                _, extention = os.path.splitext(rendition.file.name)
                attrs = [
                    f'srcset="{rendition.url}"',
                    f'media="({get_media_query(spec, rendition)})"',
                    f'type="{get_type(extention)}"',
                ]
                srcsets.append(f'<source {" ".join(attrs)} />')

        renditions = get_renditions(image, baseSpec)
        for rendition in renditions:
            _, extention = os.path.splitext(rendition.file.name)
            attrs = [
                f'srcset="{rendition.url}"',
                f'type="{get_type(extention)}"',
            ]
            srcsets.append(f'<source {" ".join(attrs)} />')
            if base is None and extention in [".jpg", ".png"]:
                base = rendition

        if base is None:
            base = renditions.pop()

        picture = f"""<picture>
    {"".join(srcsets)}

    <img src="{base.url}" alt="{base.alt}" />
    </picture>"""

        return mark_safe(picture)
