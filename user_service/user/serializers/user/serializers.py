from rest_framework.serializers import *
from django.contrib.auth import get_user_model


class GetLoginTokenSerializer(Serializer):
    email = EmailField(write_only=True, required=True)
    password = CharField(write_only=True, required=True)


class GetUserInfoSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'pk', 'email', 'first_name',
            'profile_picture', 'categories_bought',
            'coupon_balance'
        ]


class UserEditNamePictureDateSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'profile_picture', 'date_of_birth']


class EditUserSendEmailSerializer(Serializer):
    user_email = EmailField(write_only=True, required=True)


class ConfirmEditUserEmailSerializer(Serializer):
    short_code = CharField(write_only=True, required=True)


class EditUserEmailSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email']


class EditUserPasswordSerializer(Serializer):
    old_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True)
    repeat_password = CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise ValidationError('Неверно введен новый пароль.')
        if attrs['new_password'] != attrs['repeat_password']:
            raise ValidationError('Новые пароли не совпадают.')
        if attrs['new_password'].isdigit() or len(attrs['new_password']) < 8:
            raise ValidationError('Новый пароль состоит только из цифр или меньше 8 символов.')
        return attrs

