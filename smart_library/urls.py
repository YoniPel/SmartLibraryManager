"""
URL configuration for smart_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import Home, AddBookView, BookPageView, BookPageEdit, BookPageDelete, LoanedBooks

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('book/<int:pk>/view', BookPageView.as_view(), name='book_view'),
    path('book/<int:pk>/edit', BookPageEdit.as_view(), name='book_edit'),
    path('book/<int:pk>/delete', BookPageDelete.as_view(), name='book_delete'),
    path('loaned_books/', LoanedBooks.as_view(), name='loaned_books')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
