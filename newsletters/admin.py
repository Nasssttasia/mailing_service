from django.contrib import admin

from newsletters.models import Newsletter, Client


# Register your models here.
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('mailing_time', 'next_run', 'periodicity', 'mailing_status', 'letter_subject', 'owner')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'fio',)
