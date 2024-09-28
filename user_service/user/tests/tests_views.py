from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from user.models import User
from user.views.user.views import *
from user.serializers.user.serializers import *


class UserAPIViewsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="admin@admin.com",
            first_name="Admin",
            password="adminadmin",
            is_verified=True,
        )

    def setUp(self):
        login_url = "/user/api/login/"
        user_data = {
            "email": "admin@admin.com",
            "password": "adminadmin",
        }
        response = self.client.post(login_url, data=user_data, format="json")
        token = f"Q {response.data['access']}"
        session = self.client.session
        session["token"] = token
        session.save()

    def test_user_views(self):
        client = APIClient()
        token = self.client.session["token"]
        client.credentials(HTTP_AUTHORIZATION=token)

        # get user info test
        url = "/user/api/detail/"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # edit user info test
        url = "/user/api/edit-user/fn-pct/"
        serializer_data = {"first_name": "Test_name"}
        response = client.patch(url, data=serializer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # edit user send main test
        url = "/user/api/change-email/send-mail/"
        serializer_data = {"user_email": "admin@admin.com"}
        response = client.post(url, data=serializer_data, format="json")
        code = response.json()["detail"].split(" ")[-1:][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # change email check old email test
        url = "/user/api/change-email/send-mail/confirm/"
        serializer_data = {"short_code": code}
        response = client.post(url, data=serializer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # change email send mail new email
        url = "/user/api/change-email/send-mail/new-send/"
        serializer_data = {"email": "admin_test@admin.com"}
        response = client.post(url, data=serializer_data, format="json")
        code = response.json()["detail"].split(" ")[-1:][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # change email set new email
        url = "/user/api/change-email/send-mail/set-email/"
        serializer_data = {"short_code": code}
        response = client.post(url, data=serializer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # change password test
        url = "/user/api/edit-user/pass/"
        serializer_data = {
            "old_password": "adminadmin",
            "new_password": "admin_test",
            "repeat_password": "admin_test",
        }
        response = client.post(url, data=serializer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user history test
        url = "/user/api/user/orders-history/"
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
