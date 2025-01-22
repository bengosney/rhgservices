# Django
from django.urls import path
from django.views.generic.base import RedirectView

# Locals
from robots.views import robots

favicon_view = RedirectView.as_view(url="/static/pages/favicon/favicon.ico", permanent=True)

urlpatterns = [
    path("", robots, name="home"),
]
