
from django.core.management.base import BaseCommand

from newsletters.services import check_newsletter


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        check_newsletter()
