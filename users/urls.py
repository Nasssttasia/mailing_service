from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verify, send_password, UserListView, block_user

app_name = UsersConfig.name



urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/', verify, name='verify'),
    path('send_password/', send_password, name='send_password'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:pk>/', block_user, name='block_user'),
]