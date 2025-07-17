from rest_framework.permissions import BasePermission


class IsBankEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'bank_employee'
