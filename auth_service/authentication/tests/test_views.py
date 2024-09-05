import random
import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.core import mail
from django.contrib.auth.hashers import make_password

from authentication.models import User


class AuthAPITest(APITestCase):

    login_url = '/api/auth/login/'
    logout_url = '/api/auth/login/'
    registration_url = '/api/auth/registration/'

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email='admin@admin.com',
            first_name='Admin',
            password='adminadmin'
        )
        user.save()

    def setUp(self):
        session = self.client.session
        session['reg'] = {
            'email': 'test@test.com',
            'first_name': 'Test'
        }
        session.save()

    def test_registration(self):
        data = {
            'email': 'test@test.com',
            'first_name': 'Test'
        }

        response = self.client.post(self.registration_url, data)

        # Проверка введенных данных
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_registration(self, mock_send_task):
        data = {
            'password': 'a1234567',
            'password2': 'a1234567'
        }
        session = self.client.session

        full_code = make_password(str(
            random.randrange(100000, 999999
        )).encode('utf-8'))
        if full_code[-7] == '/':
            full_code[-7] = 'a'

        session['reg']['code'] = full_code
        session.save()

        short_code = full_code[len(full_code)-7:]

        confirm_url = f'/api/auth/confirm-registration/{short_code}/'
        response = self.client.post(confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        data = {
            'email': 'admin@admin.com',
            'password': 'adminadmin'
        }

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', json.loads(response.content))
        self.assertIn('refresh', json.loads(response.content))




