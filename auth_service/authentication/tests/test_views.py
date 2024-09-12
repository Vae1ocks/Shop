import datetime
import random
import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.core import mail
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils import timezone

from unittest.mock import patch

from authentication.models import User


class AuthAPITest(APITestCase):

    login_url = '/api/auth/login/'
    logout_url = '/api/auth/login/'
    registration_url = '/api/auth/registration/'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='admin@admin.com',
            first_name='Admin',
            password='adminadmin'
        )
        cls.user.save()

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
        url = reverse('authentication:registration')

        response = self.client.post(url, data)

        # Проверка введенных данных
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_registration(self):
        session = self.client.session

        short_code = str(random.randrange(100000, 999999))
        full_code = make_password(short_code)

        data = {
            'short_code': short_code
        }

        session['reg']['full_code'] = full_code

        session['reg']['email'] = self.user.email
        session['reg']['first_name'] = self.user.first_name
        session['reg']['password'] = 'adminadmin'
        session['reg']['expire_at'] = str(
            timezone.now() + datetime.timedelta(minutes=5)
        )

        session.save()

        url = reverse('authentication:confirm-registration')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('authentication.signals.current_app.send_task')
    def test_registration_set_password(self, mock_send_task):
        session = self.client.session
        session['reg']['email'] = 'test@test.com'
        session['reg']['first_name'] = 'test_name'
        session.save()

        url = reverse('authentication:set_new_password')
        data = {
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        user = User.objects.filter(email='test@test.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, session['reg']['first_name'])

        mock_send_task.assert_called_with(
            'send_data_user_create_user',
            kwargs={
                'email': session['reg']['email'],
                'first_name': session['reg']['first_name'],
                'password': user.password
            },
            queue='user_system_queue'
        )




    def test_login(self):
        data = {
            'email': 'admin@admin.com',
            'password': 'adminadmin'
        }
        url = reverse('authentication:login')

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', json.loads(response.content))
        self.assertIn('refresh', json.loads(response.content))




