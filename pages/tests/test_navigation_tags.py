# Django
from django.test import RequestFactory, TestCase

# First Party
from pages.models import InfoPage
from pages.templatetags.navigation_tags import get_site_root, has_children, has_menu_children


class GetSiteRootTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.root_page = InfoPage(title="Home", path="/", depth=1)
        self.root_page.save()

        self.info_page = InfoPage(title="Info", path="/info", depth=1)
        self.root_page.add_child(instance=self.info_page)

    def test_get_site_root_with_root_page_defined(self):
        request = self.factory.get("/")
        result = get_site_root(context={"request": request})
        self.assertIsNotNone(result)

    def test_has_menu_children_no_children(self):
        result = has_menu_children(self.info_page)
        self.assertFalse(result)

    def test_has_menu_children_no_menu_children(self):
        result = has_menu_children(self.root_page)
        self.assertTrue(result)

    def test_has_children_children(self):
        result = has_children(self.root_page)
        self.assertTrue(result)

    def test_has_children_no_children(self):
        result = has_children(self.info_page)
        self.assertFalse(result)
