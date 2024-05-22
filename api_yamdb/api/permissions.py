from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение для безопасного метода или для админа."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )
