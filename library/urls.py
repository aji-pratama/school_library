from django.urls import path

from . import api

app_name = 'library'

urlpatterns = [
    path('books/', api.BookListView.as_view(), name='book_list'),
    path('borrow/', api.BorrowListView.as_view(), name='borrow-list'),
    path('borrow/renew/<int:pk>/', api.BorrowRenewView.as_view(), name='borrow-renew'),
    path('borrow/history/', api.BorrowHistoryView.as_view(), name='borrow-history'),
    path('librarian-borrow/', api.LibrarianBorrowListView.as_view(), name='librarian-borrow-list'),
    path('librarian-borrow/<int:pk>/', api.LibrarianBorrowDetailView.as_view(), name='librarian-borrow-detail'),
]
