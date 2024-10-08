from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerModeratorAdminSuperuserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    """Разрешение для безопасного метода или для админа."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )
