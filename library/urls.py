from django.urls import path

from . import api

app_name = 'library'

urlpatterns = [
    path('books/', api.BookListView.as_view(), name='book_list'),
]
