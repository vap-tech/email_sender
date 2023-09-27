from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from slugify import slugify

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mailing.services import get_blog
from mailing.forms import ClientForm, MailingForm, FeedbackForm, ClientSetForm, BlogForm
from mailing.models import Feedback, Client, Mailing, ClientSet, LogSending, Blog


# Mixin's


class ViewMixin:

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return queryset
            queryset = queryset.filter(creator=self.request.user)
            return queryset

        queryset = queryset.filter(creator=None)
        return queryset


class CreateMixin:

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()

        return super().form_valid(form)


# Index


class IndexListView(ListView):
    model = Blog
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['rand_blog'] = Blog.objects.order_by('?')[:3]
        context_data['mailing_all'] = Mailing.objects.all().count()
        context_data['mailing_is_activ'] = Mailing.objects.filter(status=1).count()
        context_data['clients'] = Client.objects.all().count()

        return context_data


# Client


class ClientCreateView(CreateMixin, LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client-list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailing:client-detail', args=[self.kwargs.get('pk')])


class ClientListView(ViewMixin, ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client-list')


# Mailing:


class MailingCreateView(CreateMixin, LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing-all')


class MailingListView(ViewMixin, ListView):
    model = Mailing


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing-all')


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailing:mailing-update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        client_set_formset = inlineformset_factory(Mailing, ClientSet, form=ClientSetForm, extra=1)
        if self.request.method == 'POST':
            formset = client_set_formset(self.request.POST, instance=self.object)
        else:
            formset = client_set_formset(instance=self.object)

        context_data['formset'] = formset

        return context_data

    def form_valid(self, form):

        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


# Feedback


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    success_url = reverse_lazy('catalog:category')


class FeedbackListView(ListView):
    model = Feedback


# LogSending


class LogSendingListView(ViewMixin, ListView):
    model = LogSending


# Blog:


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mailing:blog-list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.creator = self.request.user
            new_blog.created_date = datetime.now()
            new_blog.save()
            return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        """Фильтрация по флагу опубликовано"""
        queryset = get_blog()
        queryset = queryset.filter(is_public=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """Счетчик просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('mailing:blog-list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
            return super().form_valid(form)

    def get_success_url(self):
        new_url = super().get_success_url()[:-4]
        new_url += self.object.slug
        return new_url


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('mailing:blog-list')
