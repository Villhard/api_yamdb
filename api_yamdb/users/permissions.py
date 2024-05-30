from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # TODO: Тут делаем обращение через константу класса
        return request.user.role == 'admin' or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # TODO: Тут делаем обращение через константу класса
        return request.user.role == 'admin' or request.user.is_superuser
