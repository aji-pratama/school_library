from django.utils import timezone
from django.utils.timezone import timedelta

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer, LibrarianBorrowSerializer
from .permissions import IsStudent, IsLibrarian


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BorrowListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = BorrowSerializer

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).order_by('-borrowed_at')


class BorrowRenewView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()

    def get_object(self):
        borrow = super().get_object()
        if borrow.user != self.request.user:
            raise PermissionDenied
        return borrow

    def update(self, request, *args, **kwargs):
        borrow = self.get_object()
        serializer = self.get_serializer(borrow, data=request.data)
        serializer.is_valid(raise_exception=True)
        if borrow.renewed_at:
            return Response({'message': 'Borrow already renewed'}, status=status.HTTP_400_BAD_REQUEST)

        borrow.due_at = timezone.now() + timedelta(days=30)
        borrow.renewed_at = timezone.now()
        borrow.save()
        return Response({'message': 'Borrow renewed successfully'})


class BorrowHistoryView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = BorrowSerializer

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user).exclude(renewed_at=None)


class LibrarianBorrowListView(generics.ListAPIView):
    permission_classes = (IsLibrarian,)
    serializer_class = LibrarianBorrowSerializer

    def get_queryset(self):
        return Borrow.objects.all().order_by('-borrowed_at')


class LibrarianBorrowDetailView(generics.RetrieveAPIView):
    permission_classes = (IsLibrarian,)
    serializer_class = LibrarianBorrowSerializer
    queryset = Borrow.objects.all()


class BorrowMarkBorrowedView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsLibrarian)
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrow = serializer.save()
        borrow.borrowed_at = timezone.now()
        borrow.due_at = timezone.now() + timedelta(days=30)
        borrow.save()
        return Response({'message': 'Book marked as borrowed successfully'}, status=status.HTTP_201_CREATED)


class BorrowMarkReturnedView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsLibrarian)
    serializer_class = BorrowSerializer
    queryset = Borrow.objects.all()
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        borrow = self.get_object()
        serializer = self.get_serializer(borrow, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        borrow.returned_at = timezone.now()
        borrow.save()
        return Response({'message': 'Book marked as returned successfully'})
