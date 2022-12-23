from rest_framework import permissions

from .models import UserRole


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        user_role = user.userrole
        if user_role and user_role.role == UserRole.ROLE_CHOICES[0][0]:
            return True
        return False


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        user_role = user.userrole
        if user_role and user_role.role == UserRole.ROLE_CHOICES[1][0]:
            return True
        return False
