import factory
from django.db.models import signals
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User, ConfirmEmailToken


class UserTests(APITestCase):
    MAIN_URL = "http://0.0.0.0:8000/api/v1/user/"

    @factory.django.mute_signals(signals.post_save)
    def setUp(self):
        self.data = {"first_name": "denis",
                     "last_name": "denis",
                     "email": "denis@denis.ru1",
                     "password": "somepassword",
                     "password2": "somepassword",
                     "company": "it",
                     "position": "it"}

        self.user_test = User.objects.create_user(email='test@test.ru', password='123test', is_active=True)
        self.user_test.save()
        self.token_user = ConfirmEmailToken.objects.create(user=self.user_test)
        self.user_1_token = Token.objects.create(user=self.user_test)
        self.confirm_data = {"email": self.user_test.email,
                             "token": self.token_user.key}
        self.confirm_data_bad = {"email": self.user_test.email,
                                 "tokens": self.token_user.key}
        self.login_data = {"email": self.user_test.email,
                           "password": self.token_user.key}
        self.login_data_error = {"email": self.user_test.email,
                                 "pasword": self.token_user.key}

    @factory.django.mute_signals(signals.post_save)
    def test_user_register(self):
        response = self.client.post(self.MAIN_URL + "register/", self.data).json()
        self.assertEqual(response['Status'], 'Registered')
        self.assertEqual(User.objects.count(), 2)

    def test_user_confirm_register(self):
        response = self.client.post(self.MAIN_URL + "register/confirm/", self.confirm_data).json()
        self.assertEqual(response['Status'], 'User confirmed')

    def test_user_confirm_register_error(self):
        response = self.client.post(self.MAIN_URL + "register/confirm/", self.confirm_data_bad).json()
        self.assertEqual(response['Need all fields'], 'email, token')

    def test_user_login_error(self):
        response = self.client.post(self.MAIN_URL + "login/", self.login_data_error).json()
        self.assertEqual(response['Need all fields'], 'email, password')

    def test_user_detail_get_error(self):
        response = self.client.get(self.MAIN_URL + "details/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
        response = self.client.get(self.MAIN_URL + "details/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_post_error(self):
        data = {
            "first_name": 'Denis',
            "position": 'Lead'
        }
        response = self.client.post(self.MAIN_URL + "details/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_post(self):
        data = {
            "first_name": 'Denis',
            "position": 'Lead'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_1_token.key)
        response = self.client.post(self.MAIN_URL + "details/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['Change info successfully'], "Denis")
