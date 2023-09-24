from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from catalog.forms import StyleFormMixin
from users.models import Country, User


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'country', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'country', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.HiddenInput()


class CountryForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Country
        fields = '__all__'
