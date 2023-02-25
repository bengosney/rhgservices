# Django

# Wagtail
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTests

# Locals
from .models import HomePage


class HomePageTests(WagtailPageTests):
    def test_can_not_create_homepage(self):
        self.assertAllowedParentPageTypes(HomePage, [Page])

    def test_can_create_homepage(self):
        self.assertCanCreateAt(Page, HomePage)
