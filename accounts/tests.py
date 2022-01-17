# import json
#
# import factory
# from django.db.models import signals
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
#
# from accounts.models import User
# from accounts.serializers import UserRegisterSerializer
#
#
# class UserRegisterTests(APITestCase):
#     MAIN_URL = "http://0.0.0.0:8000/api/v1/user/"
#
#     def setUp(self):
#         pass
#
#     @factory.django.mute_signals(signals.post_save)
#     def test_user_register(self):
#         data = {"first_name": "denis",
#                 "last_name": "denis",
#                 "email": "denis@denis.ru",
#                 "password": "somepassword",
#                 "password2": "somepassword",
#                 "company": "it",
#                 "position": "it"}
#         response = self.client.post(self.MAIN_URL + "register/", data, format='json')
#         print(response)
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         # self.assertEqual(len(response.data['results']), 2)
