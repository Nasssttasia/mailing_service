from django.urls import path

from newsletters.apps import NewsletterConfig
from newsletters.views import NewsletterCreateView, NewsletterListView, NewsletterDetailView, NewsletterUpdateView, \
    logs, create_client

app_name = NewsletterConfig.name

urlpatterns = [
                  path('', NewsletterListView.as_view(), name='list'),
                  path('<int:pk>/product/', NewsletterDetailView.as_view(), name='newsletter'),
                  path('create/', NewsletterCreateView.as_view(), name='create'),
                  path('edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit'),
                  path('logs/<int:pk>', logs, name='logs'),
                  path('create_client/', create_client, name='create_client'),

              ]