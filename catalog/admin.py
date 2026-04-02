from django.contrib import admin
from .models import Book, Location, Tag

admin.site.register(Book)
admin.site.register(Location)
admin.site.register(Tag)

