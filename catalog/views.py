from django.shortcuts import render, redirect
from . import forms
from . import services
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from . import models
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


class Home(ListView):
    model = models.Book
    ordering = ['-date_added_to_db']
    context_object_name = 'books'
    paginate_by = settings.PAGINATE_BY
    template_name = 'catalog/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get('search')

        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(isbn__icontains=search_term)
            )

        return queryset


class AddBookView(View):
    template_name = 'catalog/add_book.html'

    def get(self, request):
        return render(request, self.template_name, context={
            'isbn_form': forms.BookISBNForm(),
            'title_form': forms.BookTitleForm()
        })

    def post(self, request):
        isbn_form = forms.BookISBNForm(request.POST)
        title_form = forms.BookTitleForm(request.POST)

        book_data = None
        if "submit_isbn" in request.POST:
            book_data = self._get_data_by_isbn(request)

        elif 'submit_title' in request.POST:
            book_data = self._get_data_by_book_name(request)

        if book_data:
            self._save_book(request, book_data)
            return redirect('add_book')

        else:
            messages.info(request, 'הספר לא נמצא במאגר')
            return render(request, self.template_name, context={
                'isbn_form': isbn_form if isbn_form.is_bound else forms.BookISBNForm(),
                'title_form': title_form if title_form.is_bound else forms.BookTitleForm()
            })

    def _get_data_by_isbn(self, request):
        isbn_form = forms.BookISBNForm(request.POST)
        if isbn_form.is_valid():
            isbn = isbn_form.cleaned_data['isbn']
            return services.fetch_book_details_by_isbn(isbn)
        return None

    def _get_data_by_book_name(self, request):
        title_form = forms.BookTitleForm(request.POST)
        if title_form.is_valid():
            title = title_form.cleaned_data['title']
            return services.fetch_book_details_by_book_name(title)
        return None

    def _save_book(self, request, book_data):
        title = book_data.get('title')
        isbn = book_data.get('isbn')

        if models.Book.objects.filter(title=title, isbn=isbn).exists():
            messages.info(request, f"הספר {title} כבר קיים בספריה שלך")
            return False

        new_book = models.Book()

        # updates the values
        for key, value in book_data.items():
            if hasattr(new_book, key):
                setattr(new_book, key, value)

        new_book.save()
        messages.success(request, f'הספר {new_book.title} נשמר בהצלחה! ')
        return True


class BookPageView(DetailView):
    model = models.Book
    template_name = 'catalog/book_page_view.html'
    context_object_name = 'book'


class BookPageEdit(UpdateView):
    model = models.Book
    fields = '__all__'
    template_name = 'catalog/book_page_edit.html'


class BookPageDelete(DeleteView):
    model = models.Book
    template_name = 'catalog/book_page_delete.html'
    success_url = reverse_lazy('home')


