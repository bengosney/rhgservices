# Django
from django.template import Context, Template, TemplateSyntaxError
from django.test import Client, TestCase


class LinelessNodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def render_template(self, template_string, context={}):
        template = Template("{% load util_tags %}" + template_string)
        return template.render(Context(context))

    def test_lineless(self):
        rendered = self.render_template("{% lineless %}\n\nfoo\n\nbar\n\nbaz\n{% endlineless %}")
        self.assertEqual(rendered, "foo\nbar\nbaz")

    def test_compress_tag(self):
        rendered = self.render_template("{% compress %}  \nfoo\n bar \n\n baz \n{% endcompress %}")
        self.assertEqual(rendered, "foobarbaz")

    def test_compress_tag_empty(self):
        rendered = self.render_template("{% compress %}{% endcompress %}")
        self.assertEqual(rendered, "")

    def test_compress_tag_nested(self):
        rendered = self.render_template("{% compress %} {% compress %}  foo  {% endcompress %} {% endcompress %}")
        self.assertEqual(rendered, "foo")

    def test_compress_tag_no_end_tag(self):
        with self.assertRaises(TemplateSyntaxError):
            self.render_template("{% compress %}foo")
