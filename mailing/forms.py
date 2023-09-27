from django import forms

from mailing.models import Client, Mailing, Feedback, ClientSet, Blog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        exclude = ['creator']


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ['creator']


class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_public':
                continue
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Blog
        exclude = ['creator', 'slug', 'views_count', 'created_date']


class FeedbackForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'


class ClientSetForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ClientSet
        fields = '__all__'
