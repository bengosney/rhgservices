# Django
# Third Party
from django.test import RequestFactory, TestCase

# Wagtail
from wagtail.models import Page

from icecream import ic

# First Party
from pages.models import InfoPage
from pages.templatetags.navigation_tags import (
    breadcrumbs,
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

        site_root = Page.objects.get(id=1)

        self.root_page = InfoPage(title="Home", path="/1", depth=site_root.depth + 1)
        site_root.add_child(instance=self.root_page)
        self.root_page.save()

        self.info_page = InfoPage(title="Info", path="/1/2", depth=self.root_page.depth + 1)
        self.root_page.add_child(instance=self.info_page)
        self.info_page.save()

        self.lower_page = InfoPage(title="Lower", path="/1/2/3", depth=self.info_page.depth + 1)
        self.info_page.add_child(instance=self.lower_page)
        self.lower_page.save()

    def test_get_site_root_with_root_page_defined(self):
        request = self.factory.get("/")
        result = get_site_root(context={"request": request})
        self.assertIsNotNone(result)

    def test_has_menu_children_no_children(self):
        result = has_menu_children(self.lower_page)
        self.assertFalse(result)

    def test_has_menu_children_no_menu_children(self):
        result = has_menu_children(self.root_page)
        self.assertTrue(result)

    def test_has_children_children(self):
        result = has_children(self.root_page)
        self.assertTrue(result)

    def test_has_children_no_children(self):
        result = has_children(self.lower_page)
        self.assertFalse(result)

    def test_is_active(self):
        active = is_active(self.info_page, self.info_page)
        self.assertTrue(active)

    def test_not_is_active(self):
        active = is_active(self.info_page, self.root_page)
        self.assertFalse(active)

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

    def test_breadcrumbs_top_level(self):
        request = self.factory.get("/")
        result = breadcrumbs({"request": request})

        self.assertEqual(result["ancestors"], ())

    def test_breadcrumbs(self):
        request = self.factory.get(self.root_page.path)
        result = breadcrumbs({"request": request, "self": self.info_page})

        ic(result["ancestors"])
        self.assertNotEqual(result["ancestors"], ())
        self.assertEqual(result["ancestors"].count(), 2)
