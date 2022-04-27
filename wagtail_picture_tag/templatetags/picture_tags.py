# Standard Library
import contextlib
import hashlib
import os
import re
from io import BytesIO

# Django
from django import template
from django.core.cache import InvalidCacheBackendError, caches
from django.core.files import File
from django.utils.safestring import mark_safe

# Wagtail
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.models import Filter, Rendition

with contextlib.suppress(ImportError):
    # Third Party
    import willowavif  # noqa


register = template.Library()

spec_regex = re.compile(r"^(?P<op>\w+)((-(?P<size>\d+))(x(\d+))?)?$")


def parse_spec(spec):
    """Parse a filter specification."""
    if not (match := spec_regex.match(spec)):
        return None, None
    groups = match.groupdict()

    return groups["op"], groups["size"] or None


def get_media_query(spec, image):
    mediaquery = ""
    op, size = parse_spec(spec)

    if op in ["fill", "width"]:
        mediaquery = f"max-width: {size}px"
    elif op in ["max", "height", "scale", "original"]:
        mediaquery = f"max-width: {image.width}px"
    elif op in ["min"]:
        mediaquery = f"min-width: {size}px"

    return mediaquery


def get_avif_rendition(image, imageRendition, filter_spec):
    filterSpec = Filter(spec=filter_spec)
    cache_key = filterSpec.get_cache_key(image)
    avifSpec = "|".join([filter_spec, "format-avif"])

    try:
        avifRendition = image.get_rendition(avifSpec)
    except InvalidFilterSpecError:
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
            if cache_key:
                output_extension = f"{cache_key}.{output_extension}"
            output_filename_without_extension = input_filename_without_extension[: (59 - len(output_extension))]
            output_filename = f"{output_filename_without_extension}.{output_extension}"

            avifRendition, _ = image.renditions.get_or_create(
                filter_spec=avifSpec, focal_point_key=cache_key, defaults={"file": File(avifImage.f, name=output_filename)}
            )
    return avifRendition


def get_renditions(image, filter_spec, formats):
    """Get a list of renditions that match the filter specification."""
    if not filter_spec:
        return []

    try:
        _ = Filter(spec=filter_spec)
    except InvalidFilterSpecError:
        return []

    formats.sort(reverse=True)
    renditions = [image.get_rendition("|".join([filter_spec, f"format-{f}"])) for f in formats if f != "avif"]

    if "avif" in formats:
        with contextlib.suppress(AttributeError):
            renditions.append(get_avif_rendition(image, renditions[0], filter_spec))

    renditions.sort(key=lambda r: r.file.size)

    return renditions


@register.tag()
def picture(parser, token):
    bits = token.split_contents()[1:]
    image_expr = parser.compile_filter(bits[0])

    filter_specs = []
    formats = []
    loading = "eager"
    for spec in bits[1:]:
        if spec == "transparent":
            formats += ["png", "webp", "avif"]
        elif spec == "photo":
            formats += ["jpeg", "webp", "avif"]
        elif spec.startswith("format-"):
            formats.append(spec.split("-")[1])
        elif spec == "lazy":
            loading = "lazy"
        else:
            filter_specs.append(spec)

    if not formats:
        formats = ["webp", "jpeg", "png", "avif"]

    return PictureNode(image_expr, filter_specs, list(set(formats)), loading)


class PictureNode(template.Node):
    def __init__(self, image, specs, formats, loading):
        self.image = image
        self.specs = specs
        self.formats = formats
        self.loading = loading

        super().__init__()

    def render(self, context):
        image = self.image.resolve(context)
        if image is None:
            return ""
        try:
            cache_keys = []
            for spec in self.specs:
                f = Filter(spec=spec)
                cache_keys.append(f.get_cache_key(image))
                cache_keys.append(spec)

            cache_keys.append(image.file_hash)

            cache_key = hashlib.sha1("|".join(set(cache_keys)).encode("utf-8")).hexdigest()

            cache = caches["renditions"]
            if cached_picture := cache.get(cache_key):
                return mark_safe(cached_picture)
        except InvalidCacheBackendError:
            cache_key = None
            cache = None

        baseSpec = self.specs[0]
        sizedSpecs = self.specs[1:]
        base = None

        srcsets = []

        def get_type(ext):
            _type = "jpeg" if ext == "jpg" else ext.replace(".", "")
            return f"image/{_type}"

        sizedSpecs.sort(key=lambda spec: parse_spec(spec)[1], reverse=True)
        for spec in sizedSpecs:
            renditions = get_renditions(image, spec, self.formats)
            for rendition in renditions:
                _, extention = os.path.splitext(rendition.file.name)
                attrs = [
                    f'srcset="{rendition.url}"',
                    f'media="({get_media_query(spec, rendition)})"',
                    f'type="{get_type(extention)}"',
                    f'width="{rendition.width}"',
                    f'height="{rendition.height}"',
                ]
                if self.loading != "eager":
                    attrs.append(f'loading="{self.loading}"')

                srcsets.append(f'<source {" ".join(attrs)} />')

        renditions = get_renditions(image, baseSpec, self.formats)
        for rendition in renditions:
            _, extention = os.path.splitext(rendition.file.name)
            attrs = [
                f'srcset="{rendition.url}"',
                f'type="{get_type(extention)}"',
                f'width="{rendition.width}"',
                f'height="{rendition.height}"',
            ]
            if self.loading != "eager":
                attrs.append(f'loading="{self.loading}"')

            srcsets.append(f'<source {" ".join(attrs)} />')
            if base is None and extention in [".jpg", ".png"]:
                base = rendition

        if base is None:
            base = renditions.pop()

        attrs = [
            f'src="{base.url}"',
            f'width="{base.width}"',
            f'height="{base.height}"',
            f'alt="{base.alt}"',
        ]

        if self.loading != "eager":
            attrs.append(f'loading="{self.loading}"')

        picture = f"""<picture>
    {"".join(srcsets)}
    <img {" ".join(attrs)} />
</picture>"""

        if cache_key and cache:
            cache.set(cache_key, picture)

        return mark_safe(picture)
