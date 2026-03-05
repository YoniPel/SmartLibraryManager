from django import forms
from . import models


class BookISBNForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["isbn"]


class BookTitleForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ["title"]
