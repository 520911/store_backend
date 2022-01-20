import factory
from django.db.models import signals
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User
from orders.models import Shop


class ShopOrderTests(APITestCase):
    MAIN_URL = "http://0.0.0.0:8000/api/v1/partner/"

    @factory.django.mute_signals(signals.post_save)
    def setUp(self):
        self.user_test = User.objects.create_user(email='test@test.ru', password='123test', is_active=True, type='shop')
        self.user_test.save()
        self.user_1_token = Token.objects.create(user=self.user_test)
        self.shop_data = {
            'name': 'Test',
            'user': self.user_test
        }
        self.new_shop = Shop.objects.create(**self.shop_data)

    def test_shop_state(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get(self.MAIN_URL + 'state/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shop_state_post(self):
        data = {'state': 0}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.post(self.MAIN_URL + 'state/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.get(self.MAIN_URL + 'orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
