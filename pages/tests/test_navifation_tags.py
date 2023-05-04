# Django
from django.test import RequestFactory, TestCase

# First Party
from pages.templatetags.navigation_tags import get_site_root

# from django.contrib.sites.models import Site


class GetSiteRootTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_site_root_with_root_page_defined(self):
        request = self.factory.get("/")
        result = get_site_root(context={"request": request})
        self.assertIsNotNone(result)
