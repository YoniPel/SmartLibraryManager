from django.shortcuts import render
from . import forms


def home(request):
    return render(request, 'catalog/home.html')


def add_book(request):
    form = forms.BookISBNForm()
    return render(request, 'catalog/add_book.html', context={'form': form})