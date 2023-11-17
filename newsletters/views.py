from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from newsletters.forms import NewsletterForm
from newsletters.models import Newsletter, NewsletterLogs, Client

class OnlyForOwnerOrStaffMixin:
    def get_object(self, queryset=None):
        newsletter = super().get_object(queryset)
        if newsletter.owner == self.request.user:
            return newsletter
        if self.request.user.is_staff or self.request.user.is_superuser:
            return newsletter

class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm

    success_url = reverse_lazy('newsletters:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, OnlyForOwnerOrStaffMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletters:list')

    #def get_success_url(self):
        #return reverse('catalog:product', args=[self.kwargs.get('pk')])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object.owner != self.request.user:
            newsletter_fields = [f for f in form.fields.keys()]
            for field in newsletter_fields:
                if not self.request.user.has_perm(f'newsletters.set_{field}'):
                    del form.fields[field]
        return form




class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    permission_required = 'newsletters.list_newsletter'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    """def get_object(self, queryset=None):
        newsletter = super().get_object(queryset)
        if newsletter.owner == self.request.user:
            return newsletter
        if self.request.user.has_perm('newsletters.list_newsletter'):
            return newsletter
        raise PermissionDenied"""


class NewsletterDetailView(LoginRequiredMixin, OnlyForOwnerOrStaffMixin, DetailView):
    model = Newsletter



def logs(request, pk):
    logs = NewsletterLogs.objects.filter(pk=pk).last()
    context = {
        'object': logs,
        'date_time': 'дата и время последней попытки',
        'status': 'статус попытки',
        'mail_server_response': 'ответ почтового сервиса'
    }
    return render(request, 'newsletters/logs.html', context)


def create_client(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        fio = request.POST.get('fio')
        comment = request.POST.get('comment')
        client = Client(email=email, fio=fio, comment=comment)
        client.owner = request.user
        client.save()

    context = {
        'object': 'Клиент',
    }
    return render(request, 'newsletters/create_client.html', context)
