from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    # ограничения на уровне всего запросса, SAFE_METHODS - методы get, head, options только для чтения
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):
    # ограничение на уровне обьекта
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user