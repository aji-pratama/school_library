from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserRole(models.Model):
    ROLE_CHOICES = (
        (1, 'Student'),
        (2, 'Librarian')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    class Meta:
        unique_together = ('title', 'author',)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField()
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book',)

    def __str__(self):
        return f"{self.user} - {self.book}"
