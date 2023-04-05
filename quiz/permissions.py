from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(request.user.student)
        except Exception:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(request.user.admin)
        except Exception:
            return False