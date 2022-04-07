from rest_framework.permissions import BasePermission

class IsTeacherUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_teacher)

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_student)

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)