from django import forms
from . import models
from .models import Location


class BookISBNForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["isbn"]


class BookTitleForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["title"]


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].initial = Location.objects.get(pk=1)

