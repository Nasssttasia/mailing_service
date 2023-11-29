from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore

from newsletters.services import check_newsletter


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
          check_newsletter,
          trigger=CronTrigger(second="*/1"),  # Every 60 seconds
          id="check_newsletter_aptscheduler",  # The `id` assigned to each job MUST be unique
          max_instances=1,
          replace_existing=True,
        )


        try:
          scheduler.start()
        except KeyboardInterrupt:
          scheduler.shutdown()
