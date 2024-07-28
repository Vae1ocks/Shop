from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'first_name']


class ConfirmRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароли не совпадают.')
        if len(attrs['password']) < 8:
            raise serializers.ValidationError('Пароль слишком короткий.')
        if attrs['password'].isdigit():
            raise serializers.ValidationError('Неверно заполнен пароль.')
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)



