from django.contrib.auth.models import User

from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

from .serializers import StaffSerializer, SuperuserSerializer
from mutils.permissions import AccessUser

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUser, AccessUser]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperuserSerializer
        elif self.request.user.is_staff:
            return StaffSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

