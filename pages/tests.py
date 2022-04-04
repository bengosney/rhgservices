# Wagtail
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailPageTests

# Locals
from .models import HomePage, InfoPage


class HomePageTests(WagtailPageTests):
    def test_can_not_create_homepage(self):
        self.assertCanNotCreateAt(InfoPage, HomePage)

    def test_can_create_homepage(self):
        self.assertCanCreateAt(Page, HomePage)
