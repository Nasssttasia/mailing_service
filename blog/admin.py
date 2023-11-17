from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'img', 'date', 'is_published')
