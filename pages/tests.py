# Django
from django import forms
from django.core import mail
from django.test import TestCase

# Wagtail
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTests

# First Party
from pages.blocks import MapBlock
from pages.models import FormPage

# Locals
from .models import HomePage


class HomePageTests(WagtailPageTests):
    def test_can_not_create_homepage(self):
        self.assertAllowedParentPageTypes(HomePage, [Page])

    def test_can_create_homepage(self):
        self.assertCanCreateAt(Page, HomePage)


class FormPageTestCase(TestCase):
    def test_send_mail(self):
        form_page = FormPage(
            title="Test Form Page",
            slug="test-form-page",
            to_address="toaddress@example.com",
            from_address="noreply@example.com",
            subject="Test Form Submission",
        )
        form_data = {"name": "Test User", "email": "test@example.com", "message": "Hello World"}
        form = form_page.get_form(form_data)
        form.fields = {
            "email": forms.EmailField(),
        }
        self.assertTrue(form.is_valid())
        form_page.send_mail(form)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["toaddress@example.com"])
        self.assertEqual(mail.outbox[0].subject, "Test Form Submission")
        self.assertEqual(mail.outbox[0].reply_to, ["test@example.com"])

    def test_get_data_fields(self):
        form_page = FormPage(title="Test Form Page", slug="test-form-page")
        data_fields = form_page.get_data_fields()
        self.assertIsInstance(data_fields, list)
        for data_field in data_fields:
            self.assertIsInstance(data_field, tuple)


class MapBlockTestCase(TestCase):
    def setUp(self) -> None:
        self.values = {"title": "Test Map", "latitude": 40.712776, "longitude": -74.005974}
        self.hash = "0a2ca8e1d6f9c5c7ad9c5a8996768610"
        return super().setUp()

    def test_get_context(self):
        block = MapBlock()
        context = block.get_context(self.values)
        self.assertIn("self", context)
        self.assertIn("hash", context["self"])
        self.assertEqual(context["self"]["title"], "Test Map")
        self.assertEqual(context["self"]["latitude"], 40.712776)
        self.assertEqual(context["self"]["longitude"], -74.005974)

    def test_hash_generation(self):
        block = MapBlock()
        context1 = block.get_context(self.values)
        self.assertEqual(context1["self"]["hash"], self.hash)
