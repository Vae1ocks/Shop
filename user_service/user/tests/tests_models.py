from django.test import TestCase


from user.models import User


class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            email="admin@admin.com",
            first_name="Admin",
            password="adminadmin",
        )
        user.save()

    def test_model(self):
        user = User.objects.get(pk=1)

        self.assertEqual(user.email, "admin@admin.com")
        self.assertEqual(user.first_name, "Admin")
        self.assertEqual(user.is_verified, False)

        user.is_verified = True
        user.save()

        self.assertEqual(user.is_verified, True)
