# Django
from django.core.management.base import BaseCommand

# Wagtail
from wagtail.images.models import Rendition


class Command(BaseCommand):
    help = "Clear all the image renditions allowing any missing images to be faked"

    def handle(self, *args, **options):
        Rendition.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Removed all image renditions"))
