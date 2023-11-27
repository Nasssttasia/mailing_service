from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView



app_name = BlogConfig.name

urlpatterns = [
                  path('', cache_page(60)(BlogListView.as_view()), name='list'),
                  path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),

              ]
