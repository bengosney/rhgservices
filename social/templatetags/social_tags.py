# Django
from django import template

# Wagtail
from wagtail.models import Site

# Locals
from social.models import Social

register = template.Library()


@register.inclusion_tag("tags/social_tags.html", takes_context=True)
def social_tags(context):
    site = Site.find_for_request(context["request"])
    settings = Social.for_request(context["request"])

    context["site"] = site

    try:
        jsonld = template.Template(settings.json_ld)
        rendered_jsonld = jsonld.render(context)
    except Exception:
        rendered_jsonld = ""

    return {
        "og_description": settings.description,
        "og_image": settings.image,
        "og_title": site.site_name,
        "og_url": site.root_url,
        "jsonld": rendered_jsonld,
    }
