from django import forms
from django.core import validators
from .models import MenuItem
from django.contrib.auth.models import Group


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = 'name', 'price', 'discount', 'archived', 'preview'

    images = MultipleFileField()
