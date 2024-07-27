from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Goods, Comment, PriceHistory
from django.urls import reverse
from django.contrib.auth import get_user_model
from .serializers.store.serializers import *
from unittest.mock import patch, MagicMock
import responses


def create_category(title):
    return Category.objects.create(title=title)


class StoreTest(APITestCase):
    def user_create(self, username='username', password='89h2fffnw',
                    auth_required=True):
        user = get_user_model().objects.create_user(username=username, password=password)
        if auth_required:
            is_authenticated = self.client.login(username=username, password=password)
            self.assertTrue(is_authenticated)
        return user

    def setup(self, auth_required=True):
        self.category = Category.objects.create(title='First Category')
        self.category2 = Category.objects.create(title='Second Category')
        self.category3 = Category.objects.create(title='Third Category')
        self.goods = Goods.objects.create(title='First Goods', price='6',
                                          amount=1, category=self.category,
                                          times_bought=2)
        self.goods2 = Goods.objects.create(title='Second Goods', price='25',
                                           amount=1, category=self.category,
                                           times_bought=3)
        self.goods3 = Goods.objects.create(title='Third Goods', price='2',
                                           amount=1, category=self.category2,
                                           times_bought=8)
        self.goods4 = Goods.objects.create(title='Fourth Goods', price='10',
                                           amount=1, category=self.category3,
                                           times_bought=6)
        self.username = 'username'
        self.password = 'password123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

        if auth_required:
            is_authenticated = self.client.login(username=self.username,
                                                 password=self.password)
            self.assertTrue(is_authenticated)

    @patch('store.views.store.views.requests.get')
    def test_goods_list_no_filter(self, mock_get):
        self.setup()
        url = reverse('store:goods_list')

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {self.goods3.category.title: 15,
                                           self.goods.category.title: 2}
        mock_get.return_value = mock_response

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

        rec_data = data['recommended_goods']
        oth_data = data['other_goods']
        self.assertEqual(len(rec_data), 3)
        self.assertEqual(len(oth_data), 1)
        self.assertEqual(rec_data, GoodsListSerializer(
            [self.goods3, self.goods2, self.goods], many=True
        ).data)
        self.assertEqual(oth_data, GoodsListSerializer([self.goods4], many=True).data)

    def test_goods_list_category_filter(self):
        self.setup()
        url = reverse('store:goods_category_list', args=(self.category.title, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('goods', data)
        data = data['goods']
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], GoodsListSerializer(self.goods2).data)
        self.assertEqual(data[1], GoodsListSerializer(self.goods).data)

    @patch('store.views.store.views.requests.get')
    def test_goods_list_title_filter(self, mock_get):
        self.setup()
        url = reverse('store:goods_list')

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {self.goods3.category.title: 15,
                                           self.goods4.category.title: 2}
        mock_get.return_value = mock_response

        response = self.client.get(url, {'title': 'd Goods'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        rec_data = data['recommended_goods']
        oth_data = data['other_goods']

        self.assertEqual(len(rec_data), 1)
        self.assertEqual(len(oth_data), 1)
        self.assertEqual(rec_data, GoodsListSerializer([self.goods3], many=True).data)
        self.assertEqual(oth_data, GoodsListSerializer([self.goods2], many=True).data)

    @patch('store.views.store.views.requests.get')
    def test_goods_price_filter(self, mock_get):
        self.setup()
        url = reverse('store:goods_list')

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {self.goods3.category.title: 15,
                                           self.goods4.category.title: 2}
        mock_get.return_value = mock_response

        response = self.client.get(url, {'title': 'Goods', 'price': '5;25'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        rec_data = data['recommended_goods']
        oth_data = data['other_goods']
        for rec_goods in rec_data:
            self.assertTrue(5 <= float(rec_goods['price']) <= 25)
        for oth_goods in oth_data:
            self.assertTrue(5 <= float(oth_goods['price']) <= 25)

    def test_goods_detail(self):
        self.setup()
        url = reverse('store:goods_detail', args=(self.goods.id, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), GoodsDetailSerializer(self.goods).data)

    def test_goods_price_history(self):
        self.setup(auth_required=False)
        self.assertEqual(len(PriceHistory.objects.all()), 4)
        self.goods.price = 100
        self.goods.save()
        query = PriceHistory.objects.filter(goods=self.goods)
        self.assertEqual(len(query), 2)
        self.assertEqual(query[0].price, self.goods.price)
        self.assertEqual(len(GoodsDetailSerializer(self.goods).data['price_history']), 2)

    @patch('store.views.store.views.requests.get')
    def test_comment_create(self, mock_get):
        self.setup()
        url = reverse('store:comment_create', args=[self.goods.id])
        data = {
            'body': 'Some comment body',
            'rating': 5,
            'goods': self.goods.id
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'first_name': 'Username', 'profile_picture': None}
        mock_get.return_value = mock_response

        self.goods.users_bought.append(self.user.id)
        self.goods.save()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 5)
        comment = Comment.objects.filter(goods=self.goods.id, body=data['body']).first()
        self.assertEqual(comment.author, self.user.id)
        self.assertEqual(comment.author_name, 'Username')
        self.assertFalse(comment.author_profile_picture)

    def test_comment_partial_update(self):
        self.setup()
        comment = Comment.objects.create(author=self.user.id, author_name='Username',
                                         body='Comment body', goods=self.goods,
                                         rating=5)
        url = reverse('store:comment_edit', args=[comment.id])
        data = {
            'body': 'Some other comment body',
            'rating': 3
        }
        full_data = {'goods': self.goods4.id, **data}

        response = self.client.patch(url, full_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()

        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 3)

        for key in data:
            self.assertEqual(getattr(comment, key), data[key])
        self.assertNotEqual(comment.goods.id, full_data['goods'])
        self.assertEqual(comment.goods.id, self.goods.id)

    def test_comment_delete(self):
        self.setup()
        comment = Comment.objects.create(author=self.user.id, body='Comment body',
                                         goods=self.goods, rating=5)
        url = reverse('store:comment_edit', args=[comment.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertQuerySetEqual(Comment.objects.all(), [])
        self.goods.refresh_from_db()
        self.assertEqual(self.goods.rating, 0)