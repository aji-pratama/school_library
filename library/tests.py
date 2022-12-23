from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Borrow, UserRole

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
                print(" DUE AT BOOK", data['due_at'])
                self.assertEqual(data['due_at'], self.test_due_at)
                self.assertFalse('available_copies' in data)


class BorrowTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.user_role = UserRole.objects.create(user=self.user, role=UserRole.ROLE_CHOICES[0][0])
        self.book = Book.objects.create(
            title='Book 1', author='Test Author',
            total_copies=1, available_copies=1
        )
        self.borrow = Borrow.objects.create(
            user=self.user, book=self.book,
            borrowed_at=timezone.now(),
            due_at=timezone.now() + timedelta(days=30)
        )
        self.url = reverse('library:borrow-list')

    def test_borrow_list_authorized(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['book'], self.book.pk)
        self.assertEqual(response.data[0]['due_at'], self.borrow.due_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_borrow_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_borrow_renew_authorized(self):        
        self.client.force_authenticate(user=self.user)
        data = {'book': self.book.id, 'borrowed_at': self.borrow.borrowed_at, 'due_at': self.borrow.due_at}
        response = self.client.put(reverse('library:borrow-renew', kwargs={'pk': self.borrow.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Borrow renewed successfully')

    def test_borrow_renew_unauthorized(self):
        response = self.client.put(reverse('library:borrow-renew', kwargs={'pk': self.borrow.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
