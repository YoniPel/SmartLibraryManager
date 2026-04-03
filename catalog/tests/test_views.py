from django.test import TestCase
from django.urls import reverse

from catalog.models import Book, Location
from catalog.forms import BookTitleForm, BookISBNForm

from unittest.mock import patch

from smart_library.settings import PAGINATE_BY

class HomeViewTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="The Hobbit", author="Tolkien")

    def test_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'catalog/home.html')


    def test_view_returns_books(self):
        # This function tests that the home view returns the book objects
        response = self.client.get(reverse('home'))
        self.assertIn(self.book, response.context['books'])

    def test_view_contains_the_book_title(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.book.title)


    def test_get_queryset_returns_all_books_without_search(self):
        Book.objects.create(title="Lord Of The Rings", author="Tolkien")
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['books']), 2)

    def test_get_queryset_filters_by_title(self):
        Book.objects.create(title="Lord Of The Rings", author="Tolkien")
        response = self.client.get(reverse('home'), data={'search-title': 'Hobbit'})
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0].title, self.book.title)

    def test_get_queryset_filters_by_isbn(self):
        another_book = Book.objects.create(title="Lord Of The Rings", author="Tolkien", isbn='0123456789')
        response = self.client.get(reverse('home'), data={'search-title': another_book.isbn })
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0].title, another_book.title)


    def test_get_queryset_filters_by_author(self):
        another_book = Book.objects.create(title="Harry Potter", author="J. K. Rowling")
        response = self.client.get(reverse('home'), data={'search-author': 'J. K. Rowling'})
        self.assertEqual(len(response.context['books']), 1)
        self.assertIn(another_book, response.context['books'])

    def test_get_queryset_filters_by_location(self):
        location = Location.objects.create(name="Living Room")

        another_book = Book.objects.create(title="Harry Potter", author="J. K. Rowling", location=location)
        response = self.client.get(reverse('home'), data={'search-location': "Living Room"})

        self.assertEqual(len(response.context['books']), 1)
        self.assertIn(another_book, response.context['books'])

    def test_get_queryset_filters_by_person_loaned_to(self):
        another_book = Book.objects.create(title="Harry Potter", author="J. K. Rowling", person_loaned_to="John Doe")
        response = self.client.get(reverse('home'), data={'search-person-loaned-to': 'John Doe'})

        self.assertEqual(len(response.context['books']), 1)
        self.assertIn(another_book, response.context['books'])

    def test_get_queryset_returns_empty_then_no_book_matches(self):
        response = self.client.get(reverse('home'), data={'search-title': 'NotExist'})
        self.assertEqual(len(response.context['books']), 0)

    def test_get_queryset_filters_case_insensitively(self):
        response = self.client.get(reverse('home'), data={'search-title': 'hobbit'})
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0], self.book)

    def test_get_queryset_returns_all_books_when_search_is_empty(self):
        another_book = Book.objects.create(title="Lord Of The Rings", author="Tolkien")
        response = self.client.get(reverse('home'), data={'search-title': ''})
        self.assertIn(self.book, response.context['books'])
        self.assertIn(another_book, response.context['books'])


class AddBookViewTest(TestCase):

    def test_view_status_code(self):
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('add_book'))
        self.assertTemplateUsed(response, 'catalog/add_book.html')


    def test_get_returns_isbn_form(self):
        response = self.client.get(reverse('add_book'))
        self.assertIn('isbn_form', response.context)
        self.assertIsInstance(response.context['isbn_form'], BookISBNForm)

    def test_get_returns_title_form(self):
        response = self.client.get(reverse('add_book'))
        self.assertIn('title_form', response.context)
        self.assertIsInstance(response.context['title_form'], BookTitleForm)

    @patch('catalog.services.fetch_book_details_by_isbn')
    def test_post_adds_book_when_return_by_isbn_returns_valid_dict(self, mock_fetch):
        mock_fetch.return_value = {
            "title": "Lord Of The Rings",
            "author": "Tolkien",
            "description": "A fantasy book",
            "published_date": "1937",
            "page_count": 310,
            "cover_image": None,
            "isbn": "0123456789"
        }

        response = self.client.post(reverse('add_book'), data={
            "isbn": "0123456789",
            "submit_isbn" : True # we have `if 'submit_isbn' in request.post` in the post function
        })

        self.assertEqual(response.status_code, 302)

        mock_fetch.assert_called_once_with("0123456789")

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.first()
        self.assertEqual(book.isbn, "0123456789")

        self.assertRedirects(response, reverse('add_book'))

    @patch('catalog.services.fetch_book_details_by_isbn')
    def test_post_doesnt_add_book_when_return_by_isbn_returns_none(self, mock_fetch):
        mock_fetch.return_value = None

        response = self.client.post(reverse('add_book'), data={
            "isbn": "Non-existent isbn",
            "submit_isbn": True  # we have `if 'submit_isbn' in request.post` in the post function
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)


    @patch('catalog.services.fetch_book_details_by_book_name')
    def test_post_adds_book_when_return_by_book_name_returns_valid_dict(self, mock_fetch):
        mock_fetch.return_value = {
            "title": "Lord Of The Rings",
            "author": "Tolkien",
            "description": "A fantasy book",
            "published_date": "1937",
            "page_count": 310,
            "cover_image": None,
            "isbn": None
        }

        response = self.client.post(reverse('add_book'), data={
            "title": "Lord Of The Rings",
            "submit_title": True  # we have `if 'submit_title' in request.post` in the post function
        })

        self.assertEqual(response.status_code, 302)

        mock_fetch.assert_called_once_with("Lord Of The Rings")

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.first()
        self.assertEqual(book.title, "Lord Of The Rings")

        self.assertRedirects(response, reverse('add_book'))


    @patch('catalog.services.fetch_book_details_by_book_name')
    def test_post_doesnt_add_book_when_return_by_book_name_returns_none(self, mock_fetch):
        mock_fetch.return_value = None

        response = self.client.post(reverse('add_book'), data={
            "title": "Non-existent Book",
            "submit_title": True  # we have `if 'submit_isbn' in request.post` in the post function
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)


    @patch('catalog.services.fetch_book_details_by_isbn')
    def test_post_doesnt_save_another_book_with_matching_isbn_and_title_to_existing_one_using_isbn_form(self, mock_fetch):
        mock_fetch.return_value = {
            "title": "Lord Of The Rings",
            "isbn": "0123456789"
        }

        Book.objects.create(title="Lord Of The Rings", isbn="0123456789")

        response = self.client.post(reverse('add_book'), data={
            "isbn": "0123456789",
            "submit_isbn": True
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

        mock_fetch.assert_called_once_with("0123456789")

    @patch('catalog.services.fetch_book_details_by_book_name')
    def test_post_doesnt_save_another_book_with_matching_isbn_and_title_to_existing_one_using_title_form(self, mock_fetch):
        mock_fetch.return_value = {
            "title": "Lord Of The Rings",
            "isbn": "0123456789"
        }

        Book.objects.create(title="Lord Of The Rings", isbn="0123456789")

        response = self.client.post(reverse('add_book'), data={
            "title": "Lord Of The Rings",
            "submit_title": True
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

        mock_fetch.assert_called_once_with("Lord Of The Rings")


class BookPageViewTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Lord Of The Rings")

    def test_view_status_code(self):
        response = self.client.get(reverse('book_view', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('book_view', kwargs={'pk': self.book.pk}))
        self.assertTemplateUsed(response, 'catalog/book_page_view.html')

    def test_viewed_book_is_the_saved_book(self):
        response = self.client.get(reverse('book_view', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.context['book'], self.book)


class BookPageEditTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Lord Of The Rings")

    def test_view_status_code(self):
        response = self.client.get(reverse('book_edit', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('book_edit', kwargs={'pk': self.book.pk}))
        self.assertTemplateUsed(response, 'catalog/book_page_edit.html')


class BookPageDeleteTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title="Lord Of The Rings")

    def test_view_status_code(self):
        response = self.client.get(reverse('book_delete', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('book_delete', kwargs={'pk': self.book.pk}))
        self.assertTemplateUsed(response, 'catalog/book_page_delete.html')

    def test_delete_book_redirects_to_home_page(self):
        response = self.client.post(reverse('book_delete', kwargs={'pk': self.book.pk}), data={
            "submit" : True
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_delete_book_was_deleted(self):
        response = self.client.post(reverse('book_delete', kwargs={'pk': self.book.pk}), data={
            "submit" : True
        })
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


class LoanedBooksViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Lord Of The Rings", is_loaned=True, person_loaned_to="John Doe")

    def test_view_status_code(self):
        response = self.client.get(reverse('loaned_books'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('loaned_books'))
        self.assertTemplateUsed(response, 'catalog/loaned_books.html')


    def test_view_returns_only_loaned_books(self):
        self.another_book = Book.objects.create(title="The Hobbit")
        response = self.client.get(reverse('loaned_books'))
        self.assertIn(self.book, response.context['books'])
        self.assertEqual(len(response.context['books']), 1)


    def test_view_returns_empty_queryset_when_no_loaned_books(self):
        self.book.is_loaned = False
        self.book.person_loaned_to = None
        self.book.save()

        response = self.client.get(reverse('loaned_books'))
        self.assertEqual(len(response.context['books']), 0)

    def test_view_returns_specific_loaned_book_when_search_by_title(self):
        another_book = Book.objects.create(title="The Hobbit", is_loaned=True, person_loaned_to="John Doe")
        response = self.client.get(reverse('loaned_books'), data={'search-title': 'The Hobbit'})
        self.assertEqual(len(response.context['books']), 1)
        self.assertEqual(response.context['books'][0], another_book)

    def test_get_queryset_filters_by_author(self):
        another_book = Book.objects.create(title="Harry Potter", author="J. K. Rowling", is_loaned=True, person_loaned_to="John Doe")
        response = self.client.get(reverse('loaned_books'), data={'search-author': 'J. K. Rowling'})
        self.assertEqual(len(response.context['books']), 1)
        self.assertIn(another_book, response.context['books'])

    def test_get_queryset_filters_by_person_loaned_to(self):
        another_book = Book.objects.create(title="Harry Potter", author="J. K. Rowling", is_loaned=True, person_loaned_to="Not John Doe")
        response = self.client.get(reverse('loaned_books'), data={'search-person-loaned-to': 'Not John Doe'})

        self.assertEqual(len(response.context['books']), 1)
        self.assertIn(another_book, response.context['books'])



class PaginationTest(TestCase):

    PAGINATION = PAGINATE_BY

    def setUp(self):
        # creates 3 pages of books when the last page is with one book
        for _ in range(self.PAGINATION * 2 + 1):
            Book.objects.create(title="book")

    def test_pagination_page_1(self):
        response = self.client.get(reverse('home'))
        page_obj = response.context['page_obj']

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(page_obj.object_list), self.PAGINATION)

        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())


    def test_pagination_page_2(self):
        response = self.client.get(reverse('home'), data={'page': 2})
        page_obj = response.context['page_obj']

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(page_obj.object_list), self.PAGINATION)

        self.assertTrue(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())

    def test_pagination_page_3(self):
        response = self.client.get(reverse('home'), data={'page': 3})
        page_obj = response.context['page_obj']

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(page_obj.object_list), 1)

        self.assertFalse(page_obj.has_next())
        self.assertTrue(page_obj.has_previous())

    def test_pagination_invalid_page(self):
        response = self.client.get(reverse('home'), data={'page': 4})
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('home'), data={'page': 100})
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('home'), data={'page': -1})
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('home'), data={'page': 'abc'})
        self.assertEqual(response.status_code, 404)

    def test_pagination_with_query(self):
        # creates one page of another book
        for _ in range(self.PAGINATION + 1):
            Book.objects.create(title="another_book")

        response = self.client.get(reverse('home'), data={'search-title': 'another_book'})
        page_obj = response.context['page_obj']

        self.assertEqual(len(page_obj.object_list), self.PAGINATION)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())



