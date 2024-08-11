from rest_framework.permissions import BasePermission

from core.Utilities.JWTAuth import get_current_user


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_staff


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        user = get_current_user(token)
        request.user = user
        return user is not None
