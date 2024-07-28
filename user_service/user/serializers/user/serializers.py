from rest_framework.serializers import *
from django.contrib.auth import get_user_model


class CategoriesBoughtByUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['categories_bought']


class UserRepresentationalInfo(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'profile_picture']

