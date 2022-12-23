from django.contrib.auth import get_user_model
from django.db.models import Min

from rest_framework import serializers

from .models import Book, Borrow


User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    due_at = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'total_copies', 'available_copies', 'due_at', )

    def to_representation(self, obj):
        ret = super(BookSerializer, self).to_representation(obj)

        if obj.available_copies <= 0:
            ret.pop('available_copies')
        else:
            ret.pop('due_at')
        return ret

    def get_due_at(self, obj):
        if obj.available_copies <= 0:
            due_at = obj.borrow_set.aggregate(Min('due_at'))['due_at__min']
            return due_at


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ('id', 'book', 'borrowed_at', 'due_at', 'returned_at', 'renewed_at',)


class LibrarianBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ('id', 'user', 'book', 'borrowed_at', 'due_at', 'returned_at', 'renewed_at',)
