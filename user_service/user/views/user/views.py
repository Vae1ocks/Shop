import datetime
import random
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth import get_user_model
import requests
from rest_framework import status
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from celery import current_app
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import authenticate

from user.serializers.user.serializers import *
from user.tasks import *


class GetUserInfoView(RetrieveAPIView):
    serializer_class = GetUserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.id)
        serializer = GetUserInfoSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class EditUserNamePictureDateView(UpdateAPIView):
    serializer_class = UserEditNamePictureDateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    http_method_names = ['patch']

    def patch(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class EditUserSendEmailView(GenericAPIView):
    serializer_class = EditUserSendEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Проверка почты пользователя. Перед тем как изменить почту, необходимо '
                    'ее подтвердить. Мы высылаем проверочный код, который позже вводим.'
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('user_email')
        try:
            user = get_user_model().objects.get(email=email)
            short_code = str(random.randrange(100000, 999999))
            full_code = make_password(short_code)
            request.session['edit_user_email'] = {
                'full_code': full_code,
                'expire_at': str(datetime.datetime.now() + timezone.timedelta(minutes=5))
            }

            send_mail_task.delay(
                user_email=email,
                subject='Смена email.',
                message=f'Для смены email на сайте ххх введите код подтверждения: {short_code}'
            )
            return Response({'detail': f'Письмо отправлено на почту. Код: {short_code}'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': 'Неверно указан email.'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmEditUserEmailView(GenericAPIView):
    serializer_class = ConfirmEditUserEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Вводим проверочный код. Если он введен верно, то мы даем доступ к вводу '
                    'новой почты.'
    )
    def post(self, request, *args, **kwargs):
        short_code = request.data.get('short_code')
        full_code = request.session['edit_user_email'].get('full_code')
        if check_password(short_code, full_code):
            if request.session['edit_user_email'].get('expire_at') > str(datetime.datetime.now()):
                del request.session['edit_user_email']
                return Response({'detail': 'Код верный.'}, status=status.HTTP_200_OK)
            else:
                del request.session['edit_user_email']
                return Response({'detail': 'Срок действия кода истек'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Код введен неверно.'}, status=status.HTTP_400_BAD_REQUEST)


class SendMailNewEmailView(GenericAPIView):
    serializer_class = EditUserEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Пользователь вводит новую почту.'
    )
    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        short_code = str(random.randrange(100000, 999999))
        full_code = make_password(short_code)
        request.session['send_mail_new_email'] = {
            'full_code': full_code,
            'email': request.data.get('email'),
            'expire_at': str(datetime.datetime.now() + timezone.timedelta(minutes=5))
        }
        send_mail_task(
            user_email=user.email,
            subject='Смена email.',
            message=f''
        )
        return Response({'detail': f'Отправлено письмо на почту. Код: {short_code}'}, status=status.HTTP_200_OK)


class SetNewEmailView(GenericAPIView):
    serializer_class = ConfirmEditUserEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        full_code = request.session['send_mail_new_email'].get('full_code')
        short_code = request.data.get('short_code')
        print(short_code, full_code)
        if check_password(short_code, full_code):
            if request.session['send_mail_new_email'].get('expire_at') > str(datetime.datetime.now()):
                user.email = request.session['send_mail_new_email'].get('email')
                user.save()
                del request.session['send_mail_new_email']
                return Response({'detail': 'Пользователь поменял почту.'}, status=status.HTTP_200_OK)
            else:
                del request.session['send_mail_new_email']
                return Response({'detail': 'Срок действия кода истек.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Неверный код.'}, status=status.HTTP_400_BAD_REQUEST)


class EditUserPasswordView(GenericAPIView):
    serializer_class = EditUserPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': f'У пользователя {user.email} изменен пароль'},
                        status=status.HTTP_200_OK)


# История покупок
class UserHistoryView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(pk=self.request.user.pk)
        data = {'username': 'admin', 'password': 'admin'}
        token = {'Authorization': f'Q {str(requests.post('http://127.0.0.1:8003/payment/api/login', data).json()['access'])}'}
        url = 'http://127.0.0.1:8003/payment/order-list/'
        response = requests.get(url, headers=token)
        orders = response.json()
        return Response({'detail': {
            'user': user.email,
            'orders_list': orders
        }}, status=HTTP_200_OK)

