from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
NEWSLETTER_PERIOD = [
    (DAILY, 'Ежедневно'),
    (WEEKLY, 'Еженедельно'),
    (MONTHLY, 'Ежемесячно'),
]

NEW = 'new'
WORK = 'work'
STOP = 'stop'
NEWSLETTER_STATUS = [
    ('new', 'создана'),
    ('work', 'запущена'),
    ('stop', 'завершена'),
]

SEND = 'send'
FAILED = 'failed'
PENDING = 'pending'
REPEAT = [
    ('send', 'Отправлено'),
    ('failed', 'Не удалось отправить'),
    ('pending', 'В ожидании отправки'),
]


class Client(models.Model):
    email = models.CharField()
    fio = models.CharField(max_length=250)
    comment = models.TextField(**NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fio}'


class Newsletter(models.Model):
    mailing_time = models.TimeField(verbose_name='время рассылки', **NULLABLE)
    next_run = models.DateField(**NULLABLE)
    periodicity = models.CharField(max_length=300, choices=NEWSLETTER_PERIOD, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=50, choices=NEWSLETTER_STATUS, default='new', verbose_name='статус рассылки')
    letter_subject = models.CharField(max_length=100, verbose_name='тема письма')
    letter_body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f'{self.letter_subject}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                "set_mailing_status",
                "can change status of newsletters"
            ),
        ]


class NewsletterLogs(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, **NULLABLE)
    date_time = models.DateTimeField(verbose_name='дата и время последней попытки', **NULLABLE)
    status = models.BooleanField(default=False, verbose_name='статус попытки', **NULLABLE)
    mail_server_response = models.CharField(max_length=100, verbose_name='ответ почтового сервиса')

    def __str__(self):
        return f'{self.newsletter}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
