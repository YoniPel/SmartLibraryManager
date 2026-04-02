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
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_location = Location.objects.filter(pk=2).first()
        if default_location:
            self.fields['location'].initial = default_location