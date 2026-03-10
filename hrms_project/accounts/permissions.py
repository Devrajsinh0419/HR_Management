from rest_framework.permissions import BasePermission

from .models import User


class RoleBasedPermission(BasePermission):
    required_roles = ()

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in self.required_roles
        )


class IsAdminRole(RoleBasedPermission):
    required_roles = (User.Roles.ADMIN,)


class IsHRRole(RoleBasedPermission):
    required_roles = (User.Roles.HR,)


class IsEmployeeRole(RoleBasedPermission):
    required_roles = (User.Roles.EMPLOYEE,)


class IsAdminOrHRRole(RoleBasedPermission):
    required_roles = (User.Roles.ADMIN, User.Roles.HR)
