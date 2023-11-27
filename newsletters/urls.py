from django.urls import path
from django.views.decorators.cache import cache_page

from newsletters.apps import NewsletterConfig
from newsletters.views import NewsletterCreateView, NewsletterListView, NewsletterDetailView, NewsletterUpdateView, create_client, NewsletterLogsListView

app_name = NewsletterConfig.name

urlpatterns = [
                  path('', NewsletterListView.as_view(), name='list'),
                  path('<int:pk>/product/', cache_page(60)(NewsletterDetailView.as_view()), name='newsletter'),
                  path('create/', NewsletterCreateView.as_view(), name='create'),
                  path('edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit'),
                  path('logs/<int:pk>', NewsletterLogsListView.as_view(), name='logs'),
                  path('create_client/', create_client, name='create_client'),

              ]