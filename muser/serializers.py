from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.get(pk=instance.pk)
        Token.objects.filter(user=user).delete()
        Token.objects.create(user=user)
        return super().update(instance, validated_data)


class StaffSerializer(UserModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['password']



class SuperuserSerializer(UserModelSerializer):
    pk = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()
    password = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['pk', 'username', 'password', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'email']

class UserLikeSerializer(serializers.Serializer):
    moviename = serializers.ReadOnlyField()
    post = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()

    class Meta:
        fields = ['moviename', 'post', 'count']
