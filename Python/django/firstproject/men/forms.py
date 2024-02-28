from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Wife, Men


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
    code = 'russian'

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийкламнопрстуфхцшщъыьэюя-1234567890 '
        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только русские символы, дефис и пробел.')

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только руссие символы, дефис и пробел.'

    def __call__(self, value, *args, **kwargs):
        if not(set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория:',empty_label='Категория не выбрана')
    wife = forms.ModelChoiceField(queryset=Wife.objects.all(), required=False, label='Супруга:', empty_label='Не женат')

    class Meta:
        model = Men
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'wife', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

        labels = {
            'slug': 'URL',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов.')
        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Проверка')

