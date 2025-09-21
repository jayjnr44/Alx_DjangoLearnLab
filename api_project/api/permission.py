# from rest_framework.permissions import BasePermission

# class IsAuthorOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return True
#         # only allow edits if user is staff
#         return request.user.is_staff
