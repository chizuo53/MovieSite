from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

from .serializers import StaffSerializer, SuperuserSerializer
from mutils.permissions import AccessUser

# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    def post(self, request,*args,**kwargs):
        serializer =self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'pk': user.pk,
            'username':user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })


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

    @action(detail=False, methods=['get'], url_path='level', name='get_user_level')
    def get_user_level(self, request):
        user = request.user
        return Response({
            'pk': user.pk,
            'username':user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })
