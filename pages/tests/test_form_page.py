# Django
from django import forms
from django.core import mail
from django.test import TestCase

# First Party
from pages.models import FormPage


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
