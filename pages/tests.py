# Django
from django import forms
from django.core import mail
from django.test import TestCase

# Wagtail
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTests

# First Party
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
