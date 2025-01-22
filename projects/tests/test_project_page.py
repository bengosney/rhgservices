# Django
from django.test import RequestFactory, TestCase

# Third Party
from model_bakery import baker

# Wagtail
from wagtail.images.tests.utils import Image, get_test_image_file_jpeg
from wagtail.models import Page

# First Party
from projects.models import Project, ProjectImage, ProjectListPage


class ProjectPageTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_context(self):
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

        request = self.factory.get("/")
        context = self.list_page.get_context(request)

        self.assertQuerySetEqual(context["projectpages"].specific(), self.projects, ordered=False)


class ProjectPageImagesTestCase(TestCase):
    def setUp(self):
        self.project = Project(title="Project", path="/", depth=1)
        self.project.save()

        self.images = []
        for i in range(3):
            img = Image.objects.create(title="Test image", file=get_test_image_file_jpeg(f"test-{i}.jpg"))
            self.images.append(baker.make(ProjectImage, project=self.project, image=img))

    def test_banner_image(self):
        self.assertIsNotNone(self.project.banner_image())
        self.assertEqual(self.project.banner_image(), self.images[0].image)

    def test_banner_image_hero(self):
        hero = self.images[-1]
        self.project.hero_image = hero.image

        self.assertIsNotNone(self.project.banner_image())
        self.assertEqual(self.project.banner_image(), hero.image)
