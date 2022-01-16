from rest_framework.test import APITestCase
from orders.models import Shop, Category

# class ShopTests(APITestCase):
#
#     def test_create_user(self):
#         url = reverse('register-list')
#         data = {'first_name': 'denis',
#                 'last_name': 'denis',
#                 'email': 'denis@denis.ru',
#                 'password': '123',
#                 'company': 'it',
#                 'position': 'it'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ShopTests(APITestCase):
    MAIN_URL = 'http://0.0.0.0:8000/api/v1/'

    def setUp(self):
        Shop.objects.create(name='Shop1')
        Shop.objects.create(name='Shop2')

    def test_shop_list(self):
        response = self.client.get(self.MAIN_URL + 'shops/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)


class CategoryTests(APITestCase):
    MAIN_URL = 'http://0.0.0.0:8000/api/v1/'

    def setUp(self):
        shop = Shop.objects.create(name='Shop1')
        category = Category.objects.create(name='Category1')
        category.shops.set([shop])

    def test_category_list(self):
        response = self.client.get(self.MAIN_URL + 'categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
