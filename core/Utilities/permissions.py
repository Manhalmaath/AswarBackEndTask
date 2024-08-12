from rest_framework.permissions import BasePermission

from core.Utilities.JWTAuth import get_current_user


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        user = get_current_user(token)
        request.user = user
        return user is not None
