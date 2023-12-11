from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.profile.account_type == 2


class IsMaintainer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.profile.account_type == 3


class IsSeeker(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.profile.account_type == 1
