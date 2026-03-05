from django.shortcuts import render, redirect
from . import forms
from . import services
from django.contrib import messages
from . import models


def home(request):
    return render(request, 'catalog/home.html')


def add_book(request):
    isbn_form = forms.BookISBNForm()
    title_form = forms.BookTitleForm()

    if request.method == 'POST':
        book_data = None

        if "submit_isbn" in request.POST:
            isbn_form = forms.BookISBNForm(request.POST)
            if isbn_form.is_valid():
                isbn = isbn_form.cleaned_data['isbn']
                book_data = services.fetch_book_details_by_isbn(isbn)

        elif 'submit_title' in request.POST:
            title_form = forms.BookTitleForm(request.POST)
            if title_form.is_valid():
                title = title_form.cleaned_data['title']
                book_data = services.fetch_book_details_by_book_name(title)

        if book_data:

            title = book_data.get('title')
            isbn = book_data.get('isbn')

            if models.Book.objects.filter(title=title, isbn=isbn).exists():
                messages.warning(request, "הספר כבר קיים בספריה שלך")
                return redirect('add_book')

            new_book = models.Book()
            new_book.title = book_data['title']
            new_book.author = book_data['author']
            new_book.description = book_data['description']
            new_book.published_date = book_data['published_date']
            new_book.page_count = book_data['page_count']
            new_book.cover_image = book_data['cover_image']
            new_book.isbn = book_data['isbn']
            new_book.save()
            messages.success(request, f'הספר {new_book.title} נשמר בהצלחה! ')
            return redirect('home')

        else:
            messages.error(request, 'הספר לא נמצא במאגר')

    else:
        isbn_form = forms.BookISBNForm()
        title_form = forms.BookTitleForm()

    context = {
        'isbn_form': isbn_form,
        'title_form': title_form
    }
    return render(request, 'catalog/add_book.html', context=context)
