from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from .permissions import IsStudent


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = BorrowSerializer

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrowed_at')
