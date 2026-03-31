from django.db import models
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name="מיקום")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "מיקום"
        verbose_name_plural = "מיקומים"
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="כותרת")
    author = models.CharField(max_length=100, verbose_name="מחבר")
    description = models.TextField(blank=True, null=True, verbose_name="תיאור")

    published_date = models.CharField(max_length=20, blank=True, null=True, verbose_name="תאריך הוצאה")
    page_count = models.IntegerField(blank=True, null=True, verbose_name="מספר עמודים")
    cover_image = models.URLField(blank=True, null=True, verbose_name="תמונת כריכה")
    cover_image_file = models.ImageField(
        blank=True, null=True,
        upload_to='book_images/', verbose_name='תמונת כריכה ידנית'
    )

    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="מיקום")

    is_loaned = models.BooleanField(default=False, help_text='האם הספר כרגע מושאל למישהו', verbose_name='מושאל?')
    person_loaned_to = models.CharField(null=True, blank=True, verbose_name='שם השואל')

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
        return reverse('book_view', kwargs={
            'pk': self.pk
        })

    def save(self, *args, **kwargs):

        if self.person_loaned_to:
            self.is_loaned = True
            self.location = None

        else:
            self.is_loaned = False
            self.person_loaned_to = None


        super().save(*args, **kwargs)

    @property
    def get_cover_image(self):
        if self.cover_image_file:
            return self.cover_image_file.url

        if self.cover_image:
            return self.cover_image

        return "/static/catalog/assets/placeholder.jpg"

