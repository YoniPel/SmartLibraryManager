from django.test import TestCase
from catalog.forms import BookISBNForm, BookTitleForm, BookForm
from catalog.models import Location

class BookISBNFormTest(TestCase):

    def test_isbn_form_has_only_isbn_field(self):
        isbn_form = BookISBNForm(data={'isbn': '0123456789'})
        self.assertEqual(list(isbn_form.fields.keys()), ['isbn'])

    def test_isbn_form_is_valid_with_valid_isbn(self):
        isbn_form = BookISBNForm(data={'isbn': '0123456789'})
        self.assertTrue(isbn_form.is_valid())

    def test_isbn_form_is_valid_without_isbn(self):
        isbn_form = BookISBNForm(data={})
        self.assertTrue(isbn_form.is_valid())

    def test_isbn_field_is_not_required(self):
        isbn_form = BookISBNForm()
        self.assertFalse(isbn_form.fields['isbn'].required)


    def test_isbn_form_is_invalid_when_isbn_is_to_long(self):
        isbn_form = BookISBNForm(data={'isbn': '01234567890123456789'})
        self.assertFalse(isbn_form.is_valid())
        self.assertIn('isbn', isbn_form.errors)


class BookTitleFormTest(TestCase):

    def test_title_form_has_only_title_field(self):
        title_form = BookTitleForm(data={'title': "The Hobbit"})
        self.assertEqual(list(title_form.fields.keys()), ['title'])

    def test_title_form_is_valid_with_valid_title(self):
        title_form = BookTitleForm(data={'title': "The Hobbit"})
        self.assertTrue(title_form.is_valid())

    def test_title_form_is_invalid_without_title(self):
        title_form = BookTitleForm(data={})
        self.assertFalse(title_form.is_valid())
        self.assertIn('title', title_form.errors)

    def test_title_field_is_required(self):
        title_form = BookTitleForm()
        self.assertTrue(title_form.fields['title'].required)


class BookFormTest(TestCase):

    def test_book_form_is_valid_with_only_title_field(self):
        book_form = BookForm(data={'title': "The Hobbit"})
        self.assertTrue(book_form.is_valid())

    def test_book_form_author_field_is_required(self):
        book_form = BookForm()
        self.assertTrue(book_form.fields['title'].required)


    def test_book_form_is_invalid_without_any_field(self):
        book_form = BookForm(data={})
        self.assertFalse(book_form.is_valid())

    def test_book_form_is_invalid_with_fields_that_are_not_the_title_field(self):
        book_form = BookForm(data={'author': "J.R.R. Tolkien", 'description': "The Hobbit", 'page_count': "0",
                                   'isbn': "0123456789"})
        self.assertFalse(book_form.is_valid())
        self.assertIn('title', book_form.errors)

    def test_book_form_has_default_location_when_location_exists(self):
        location = Location(name="Living Room")
        location.pk = 2
        location.save()

        book_form = BookForm()
        self.assertEqual(book_form.fields['location'].initial, location)

    def test_book_form_does_not_have_default_location_when_location_does_not_exist(self):
        book_form = BookForm()
        self.assertIsNone(book_form.fields['location'].initial)









