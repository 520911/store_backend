# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from accounts.models import User, Contact
#
#
# class UserTests(APITestCase):
#
#     def setUp(self):
#         User.objects.create(
#             first_name='denis',
#             last_name='denis',
#             email='denis@denis.ru',
#             password='123',
#             company='it',
#             position='it'
#         )
#
#     def test_create_user(self):
#         response = self.client.get('register/')
#         print(response)
