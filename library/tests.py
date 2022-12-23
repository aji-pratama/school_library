from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Borrow

User = get_user_model()


class BookListTests(APITestCase):
    test_due_at = timezone.now() + timedelta(weeks=2)

    def setUp(self):
        self.book1 = Book.objects.create(title='Book 1', author='Author 1', total_copies=2, available_copies=2)
        self.book2 = Book.objects.create(title='Book 2', author='Author 2', total_copies=1, available_copies=0)
        self.user = User.objects.create_user(username='user', password='password')
        self.borrow1 = Borrow.objects.create(user=self.user, book=self.book2, borrowed_at=timezone.now(), due_at=self.test_due_at)

    def test_available_book(self):
        url = reverse('library:book_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for data in response.data:
            if data['title'] == 'Book 1':
                self.assertEqual(data['available_copies'], 2)
                self.assertFalse('due_at' in data)
            elif data['title'] == 'Book 2':
                self.assertEqual(data['due_at'], self.test_due_at)
                self.assertFalse('available_copies' in data)
