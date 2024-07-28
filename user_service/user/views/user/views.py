from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth import get_user_model
import requests
from rest_framework import status
from rest_framework import permissions

from user.serializers.user.serializers import *


# View для межсервисного взаимодействия, используется в store_service в GoodsListView
class CategoriesBoughByUserView(RetrieveAPIView):
    serializer_class = CategoriesBoughtByUserSerializer
    queryset = get_user_model().objects.all()


# View для межсервисного взаимодействия, используется в store_service в CommentCreateView
class UserRepresentationalView(RetrieveAPIView):
    serializer_class = UserRepresentationalInfo
    queryset = get_user_model().objects.all()



