import secrets

from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm, StyleFormMixin
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify')

    def form_valid(self, form):
        self.object = form.save()
        code = secrets.token_urlsafe(nbytes=7)
        self.object.code = code
        send_mail(
            subject='Подтвердите почту',
            message=f'Добро пожаловать! Чтобы подтвердить вашу почту введите код {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        self.object.save()
        return super().form_valid(form)


def verify(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user.code == code:
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))
    return render(request, 'users/verify.html')


def send_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user.email == email:
            new_password = secrets.token_urlsafe(nbytes=5)
            user.set_password(new_password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Здравствуйте! Используйте новый пароль: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            return redirect(reverse('users:login'))
    return render(request, 'users/send_password.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        newsletter_fields = [f for f in form.fields.keys()]
        for field in newsletter_fields:
            if self.request.user.has_perm(f'users.set_{field}'):
                return form


class UserListView(ListView):
    model = User


def block_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:user_list')






