# Django
from django.http import HttpResponse

# Locals
from .models import Robots


def robots(request):
    robots_txt = Robots.for_request(request)

    return HttpResponse(robots_txt.contents, content_type="text/plain")
