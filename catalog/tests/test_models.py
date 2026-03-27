from django.test import TestCase
from catalog.models import Book
from django.urls import reverse

class BookTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="The Hobbit", author="Tolkien")


    def test_str_returns_title(self):
        self.assertEqual(str(self.book), "The Hobbit")


    def test_get_absolute_url_returns_book_url(self):
        expected_url = reverse('book_view', kwargs={'pk': self.book.pk})
        self.assertEqual(self.book.get_absolute_url(), expected_url)


    def test_save_sets_is_loaned_to_true_when_person_loaned_to_exists(self):
        self.book.is_loaned = False
        self.book.person_loaned_to = "John Doe"
        self.book.save()
        self.assertTrue(self.book.is_loaned)

    def test_save_sets_is_loaned_to_false_when_person_loaned_to_is_none(self):
        self.book.is_loaned = True
        self.book.person_loaned_to = None
        self.book.save()
        self.assertFalse(self.book.is_loaned)


    def test_get_cover_image_returns_uploaded_file_url_when_file_exists(self):
        self.book.cover_image_file = "book_images/cover_image_file.jpg"
        self.book.cover_image = "https://example.com/cover_image.jpg"
        self.assertIn("cover_image_file.jpg", self.book.get_cover_image)

    def test_get_cover_image_returns_external_url_when_only_cover_image_exists(self):
        self.book.cover_image = "https://example.com/cover_image.jpg"
        self.assertEqual(
            self.book.get_cover_image,
            "https://example.com/cover_image.jpg"
        )

    def test_get_cover_image_returns_placeholder_when_no_image_exists(self):
        expected_url = "/static/catalog/assets/placeholder_image.jpg"
        self.assertEqual(self.book.get_cover_image, expected_url)


    def test_save_sets_location_to_none_when_person_loaned_to_exists(self):
        self.book.location = "shelf A"
        self.book.person_loaned_to = "John Doe"
        self.book.save()
        self.assertIsNone(self.book.location)






