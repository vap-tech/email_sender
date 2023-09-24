from random import randint
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from users.forms import CountryForm, UserRegisterForm, UserProfileForm
from users.models import Country, User


def gen_secret():
    return ''.join([str(randint(0, 9)) for _ in range(8)])

# Country


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('users:country-list')


class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm
    success_url = reverse_lazy('users:country-list')


class CountryDeleteView(DeleteView):
    model = Country
    success_url = reverse_lazy('users:country-list')


class CountryDetailView(DetailView):
    model = Country


class CountryListView(ListView):
    model = Country


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):

        new_user = form.save()
        new_user.verification_code = gen_secret()
        new_user.is_active = False
        new_user.save()

        send_mail(
            'Регистрация на v-petrenko.ru',
            f'''Привет, вот твоя ссылка для подтверждения регистрации:
             vds.v-petrenko.ru/users/{new_user.pk}/verification/{new_user.verification_code}/''',
            'admin@v-petrenko.ru',
            [new_user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class Verification(DetailView):
    model = User
    template_name = 'users/verification.html'

    def get_queryset(self):
        """Верификация"""

        queryset = super().get_queryset()

        if User.objects.filter(pk=self.kwargs['pk']).get().verification_code == self.kwargs['v_cod']:
            User.objects.filter(pk=self.kwargs['pk']).update(is_active=True)

        return queryset


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Чтобы не передавать во view pk"""
        return self.request.user


def generate_new_password(request):
    new_password = gen_secret()

    send_mail(
        'Сброс пароля на v-petrenko.ru',
        f'''Привет, твой новый пароль: {new_password}''',
        'admin@v-petrenko.ru',
        [request.user.email],
        fail_silently=False,
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:category'))
