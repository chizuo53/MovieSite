from rest_framework.permissions import BasePermission

class AccessUser(BasePermission):
    def has_permission(self, request, view):
        if (view.name == 'user_level' and request.method == 'GET') or \
        (view.name == 'user_like' and request.method in ['GET','DELETE','PUT']) or \
        (view.name == 'movieinlike' and request.method == 'GET'):
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj and request.method == 'PATCH':
            return True
        else:
            return False

class AccessSpider(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

