from rest_framework.generics import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import *
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers.social import serializers
from authentication.social_services.google import check_google_token


class GoogleAuth(GenericAPIView):
    serializer_class = serializers.GoogleAuthSerializer

    @extend_schema(
        description='Для аутентификации по гуглу'
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = check_google_token(serializer)
            token = RefreshToken.for_user(user)
            token.payload.update(
                {
                    'user_id': user.pk,
                }
            )
            return Response({
                'refresh': str(token),
                'access': str(token.access_token)
            }, HTTP_200_OK)
        else:
            return AuthenticationFailed('Некорректные данные', HTTP_403_FORBIDDEN)

