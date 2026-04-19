from rest_framework import permissions 

class IsAdmin(permissions.BasePermission):
    """Only adminz can access"""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
        
class IsLibrarian(permissions.BasePermission):
    """Only librarians or admin can access"""
    
    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
          return False
        
        return request.user.role in ["admin", "librarian"]
    
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admins can do anything
    Others can only read (GET, HEAD, OPTIONS)
    """
    
    def has_permissions(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return (
            request.user and
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

# from rest_framework import permissions


# class HasBookPermission(permissions.BasePermission):
#     """
#     Check if user has the required permission for books
    
#     - POST (create): requires 'add_book'
#     - PUT/PATCH (update): requires 'change_book'
#     - DELETE: requires 'delete_book'
#     - GET: requires 'view_book'
#     """
    
#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False
        
#         # Mapping HTTP methods to permissions
#         permission_map = {
#             'GET': 'lib.view_book',
#             'POST': 'lib.add_book',
#             'PUT': 'lib.change_book',
#             'PATCH': 'lib.change_book',
#             'DELETE': 'lib.delete_book',
#         }
        
#         required_perm = permission_map.get(request.method)
        
#         if not required_perm:
#             return False
        
#         return request.user.has_perm(required_perm)


# class CanBanBook(permissions.BasePermission):
#     """Custom permission for banning books"""
    
#     def has_permission(self, request, view):
#         return request.user.has_perm('lib.can_ban_book')





# class IsOwnerOrReadOnly(permissions.BasePermission): 
#     """
#         Object owner can edit
#         Others can only read
#     """
    
#     def has_permissions(self, request, view, obj):
        
#         safe_methods = ["GET", "HEAD", "OPTIONS"]
        
#         if request.method in safe_methods:
#             return True 
        
#         return (
#             request.user and
#             request.user.is_authenticated and
#             request.user.role == ''
#         )

    