import json

import factory
from django.db.models import signals
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User
from orders.models import Shop, Category, Order


class ShopTests(APITestCase):
    MAIN_URL = 'http://0.0.0.0:8000/api/v1/'

    def setUp(self):
        Shop.objects.create(name='Shop1')
        Shop.objects.create(name='Shop2')

    def test_shop_list(self):
        response = self.client.get(self.MAIN_URL + 'shops/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class CategoryTests(APITestCase):
    MAIN_URL = 'http://0.0.0.0:8000/api/v1/'

    def setUp(self):
        shop = Shop.objects.create(name='Shop1')
        category = Category.objects.create(name='Category1')
        category.shops.set([shop])

    def test_category_list(self):
        response = self.client.get(self.MAIN_URL + 'categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class OrderTests(APITestCase):
    MAIN_URL = 'http://0.0.0.0:8000/api/v1/'

    @factory.django.mute_signals(signals.post_save)
    def setUp(self):
        self.user_test = User.objects.create_user(email='test@test.ru', password='123test', is_active=True)
        self.user_test.save()
        self.user_1_token = Token.objects.create(user=self.user_test)
        self.data = {
            'id': self.user_test.id,
            'state': 'new'
        }

    def test_order_error_list(self):
        response = self.client.get(self.MAIN_URL + 'order/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get(self.MAIN_URL + 'order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.post(self.MAIN_URL + 'order/', self.data, format='json')
        print(response)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(Order.objects.count(), 1)
