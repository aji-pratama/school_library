from django.contrib import admin

from library.models import UserRole, Book, Borrow


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    pass
