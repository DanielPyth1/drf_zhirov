from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Кастомное разрешение, позволяющее доступ только модераторам.
    """
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь модератором
        return request.user.groups.filter(name='Модераторы').exists()


from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
