from django.db import models
from django.urls import reverse


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="כותרת")
    author = models.CharField(max_length=100, verbose_name="מחבר")
    description = models.TextField(blank=True, null=True, verbose_name="תיאור")

    published_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="תאריך הוצאה")
    page_count = models.IntegerField(blank=True, null=True, verbose_name="מספר עמודים")
    cover_image = models.URLField(blank=True, null=True, verbose_name="תמונת כריכה")

    isbn = models.CharField(max_length=13, blank=True, null=True, verbose_name="isbn")

    date_added_to_db = models.DateTimeField(auto_now_add=True, verbose_name="תאריך הוספה למערכת")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="תאריך שינוי אחרון")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ספר"
        verbose_name_plural = "ספרים"
        ordering = ["-date_added_to_db", "author"]

        unique_together = ('title', 'isbn')

    def get_absolute_url(self):
        return reverse(f'book_view', kwargs={
            'pk': self.pk
        })