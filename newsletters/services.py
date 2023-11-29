from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.core.mail import send_mail

from config import settings
from newsletters.models import Newsletter, NewsletterLogs


def check_newsletter():
    newsletters = Newsletter.objects\
        .filter(mailing_status='new')\
        .filter(mailing_time__lte=datetime.now().time())\
        .filter(next_run__lte=datetime.now().date())
    print(newsletters)

    for newsletter in newsletters:
        newsletter.mailing_status = 'work'
        newsletter.save()
        clients = newsletter.clients.all()

        emails = [str(client.email) for client in clients]
        print(emails)
        main_status = send_mail(
            subject=newsletter.letter_subject,
            message=newsletter.letter_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False
        )


        if main_status == 1:
            NewsletterLogs.objects.create(
                status=True,
            )


        if newsletter.periodicity == 'daily':
            newsletter.next_run += timedelta(days=1)
        if newsletter.periodicity == 'weekly':
            newsletter.next_run += timedelta(days=7)
        if newsletter.periodicity == 'monthly':
            newsletter.next_run += relativedelta(months=1)


        newsletter.mailing_status = 'new'
        newsletter.save()
