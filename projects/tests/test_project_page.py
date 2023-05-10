# Django
from django.test import RequestFactory, TestCase

# Wagtail
from wagtail.models import Page

# First Party
from projects.models import Project, ProjectListPage


class ProjectPageTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        site_root = Page.objects.get(id=1)

        self.list_page = ProjectListPage(title="Home", path="/1", depth=site_root.depth + 1)
        site_root.add_child(instance=self.list_page)

        for i in range(5):
            project = Project(title=f"Project not in list {i}", path=f"/1/pnil{i}", depth=self.list_page.depth + 1)
            site_root.add_child(instance=project)

        self.projects = []
        for i in range(5):
            project = Project(title=f"Project {i}", path=f"/1/p{i}", depth=self.list_page.depth + 1)
            self.list_page.add_child(instance=project)
            self.projects.append(project)

    def test_get_context(self):
        request = self.factory.get("/")
        context = self.list_page.get_context(request)

        self.assertQuerySetEqual(context["projectpages"].specific(), self.projects, ordered=False)
