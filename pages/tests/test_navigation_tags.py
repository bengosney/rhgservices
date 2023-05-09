# Django
from django.test import RequestFactory, TestCase

# First Party
from pages.models import InfoPage
from pages.templatetags.navigation_tags import (
    get_site_root,
    has_children,
    has_menu_children,
    is_active,
    top_menu,
    top_menu_children,
)


class NavigationTagsTests(TestCase):
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

    def test_is_active(self):
        active = is_active(self.info_page, self.info_page)
        self.assertTrue(active)

    def test_not_is_active(self):
        active = is_active(self.info_page, self.root_page)
        self.assertTrue(active)

    def test_top_menu(self):
        request = self.factory.get("/")
        result = top_menu({"request": request}, self.root_page)

        self.assertEqual(len(result["menuitems"]), 1)
        self.assertEqual(result["menuitems"][0].title, self.info_page.title)

    def test_top_menu_children(self):
        request = self.factory.get("/")
        result = top_menu_children({"request": request}, self.root_page)

        self.assertEqual(len(result["menuitems_children"]), 1)
        self.assertEqual(result["parent"].title, self.root_page.title)
        self.assertEqual(result["menuitems_children"][0].title, self.info_page.title)
