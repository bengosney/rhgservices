# Django
from django.template import Context
from django.test import RequestFactory, TestCase

# Wagtail
from wagtail.images.tests.utils import Image, get_test_image_file_jpeg
from wagtail.models import Site
from wagtail.tests.utils import WagtailTestUtils

# First Party
from social.models import Social
from social.templatetags.social_tags import social_tags


class SocialTagsTestCase(WagtailTestUtils, TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.img = Image.objects.create(title="Test image", file=get_test_image_file_jpeg("test.png"))

        self.site = Site.objects.get(hostname="localhost")
        self.social = Social.objects.create(
            site=self.site,
            description="Test description",
            image=self.img,
            json_ld='{ "test": "json-ld", "name": "{{ site.site_name }}" }',
        )

    def test_social_tags(self):
        request = self.factory.get("/")
        request.site = self.site
        response = social_tags(Context({"request": request}))

        self.assertEqual(response["og_description"], "Test description")
        self.assertEqual(response["og_image"], self.img)
        self.assertEqual(response["og_title"], self.site.site_name)
        self.assertEqual(response["og_url"], self.site.root_url)
        self.assertIn('"test": "json-ld"', response["jsonld"])
        self.assertIn(self.site.site_name, response["jsonld"])
