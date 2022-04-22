# Django
from django import template

register = template.Library()


@register.simple_tag
def picture(image):
    newImage = image.get_rendition("fill-802x600|format-jpeg")
    with image.get_willow_image() as willow:
        willow.save_as_avif()
    print(newImage.url)
    print(type(newImage))
    return "picture"
