from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse

from store.models import Category, Goods
from .serializers.favorites.serializers import FavoriteSerializer
from .models import Favorite

User = get_user_model()


def user_create(username="Test", password="password12345") -> User:
    return User.objects.create_user(
        username=username,
        password=password,
    )


def category_create(title="Test Category") -> Category:
    return Category.objects.create(title=title)


def goods_create(
    category=None,
    title="Test Goods",
    amount=1,
    description="This is test goods",
    price=100,
    **kwargs
) -> Goods:
    if not category:
        category = Category.objects.first()
    return Goods.objects.create(
        category=category,
        title=title,
        amount=amount,
        description=description,
        price=price,
        **kwargs
    )


class FavoritesAPITest(APITestCase):
    @classmethod
    def setUp(cls):
        cls.username = "Test User"
        cls.password = "password12345"
        cls.user = user_create(
            username=cls.username,
            password=cls.password,
        )
        category1 = category_create(title="First Category")
        category2 = category_create(
            title="Second Category",
        )
        goods = goods_create(category=category1)
        goods = goods_create(
            category=category1,
            title="Scnd Test Goods",
        )
        goods = goods_create(category=category2)

    def auth(self, username=None, password=None) -> None:
        if not username:
            username = self.username
        if not password:
            password = self.password

        is_authenticated = self.client.login(
            username=username,
            password=password,
        )
        self.assertTrue(is_authenticated)

    def test_create_favorite(self):
        user = User.objects.get(username=self.username)
        self.auth()
        goods = Goods.objects.latest("id")

        url = reverse("favorites:create")
        data = {"goods_id": goods.id}

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        is_favorite_exists = Favorite.objects.filter(
            user_id=user.id, goods=goods
        ).exists()
        self.assertTrue(is_favorite_exists)

    def test_create_clone_favorites_validation_error(self):
        user = User.objects.get(username=self.username)
        self.auth()
        goods = Goods.objects.first()
        favorite = Favorite.objects.create(
            user_id=user.id,
            goods=goods,
        )

        url = reverse("favorites:create")
        data = {"goods_id": goods.id}

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_favorites_list(self):
        user = User.objects.get(username=self.username)
        self.auth()
        goods1 = Goods.objects.first()
        goods2 = Goods.objects.latest("id")
        favorite1 = Favorite.objects.create(
            user_id=user.id,
            goods=goods1,
        )
        favorite2 = Favorite.objects.create(
            user_id=user.id,
            goods=goods2,
        )
        fake_users_favorite1 = Favorite.objects.create(
            user_id=123,
            goods=goods1,
        )
        fake_users_favorite2 = Favorite.objects.create(
            user_id=123,
            goods=goods2,
        )

        url = reverse("favorites:list")

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.json()
        self.assertEqual(len(data), 2)
        serializer = FavoriteSerializer(
            [favorite1, favorite2],
            many=True,
        )
        self.assertListEqual(data, serializer.data)

    def test_user_list_unauthorized(self):
        url = reverse("favorites:list")

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_favorite_delete(self):
        user = User.objects.get(username=self.username)
        self.auth()
        goods1 = Goods.objects.first()
        goods2 = Goods.objects.latest("id")
        favorite1 = Favorite.objects.create(
            user_id=user.id,
            goods=goods1,
        )
        favorite2 = Favorite.objects.create(
            user_id=user.id,
            goods=goods2,
        )
        fake_users_favorite1 = Favorite.objects.create(
            user_id=123,
            goods=goods1,
        )
        fake_users_favorite2 = Favorite.objects.create(
            user_id=123,
            goods=goods2,
        )

        url = reverse("favorites:delete", args=(favorite1.id,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        queryset = Favorite.objects.all()
        self.assertEqual(queryset.count(), 3)

        url = reverse("favorites:delete", args=(favorite2.id,))
        response = self.client.delete(url)
        self.assertEqual(queryset.count(), 2)
        self.assertFalse(queryset.filter(user_id=user.id).exists())

    def test_favorite_delete_forbidden(self):
        user = User.objects.get(username=self.username)
        self.auth()
        goods1 = Goods.objects.first()
        goods2 = Goods.objects.latest("id")
        fake_users_favorite1 = Favorite.objects.create(
            user_id=123,
            goods=goods1,
        )
        fake_users_favorite2 = Favorite.objects.create(
            user_id=123,
            goods=goods2,
        )

        url = reverse(
            "favorites:delete",
            args=(fake_users_favorite1.id,),
        )

        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(Favorite.objects.all().count(), 2)
