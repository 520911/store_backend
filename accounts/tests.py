import factory
from django.db.models import signals
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
        self.confirm_data = {"email": self.user_test.email,
                             "token": self.token_user.key}
        self.confirm_data_bad = {"email": self.user_test.email,
                                 "tokens": self.token_user.key}

    @factory.django.mute_signals(signals.post_save)
    def test_user_register(self):
        response = self.client.post(self.MAIN_URL + "register/", self.data).json()
        self.assertEqual(response['Status'], 'Registered')

    def test_user_confirm_register(self):
        response = self.client.post(self.MAIN_URL + "register/confirm/", self.confirm_data).json()
        self.assertEqual(response['Status'], 'User confirmed')

    def test_user_confirm_register_error(self):
        response = self.client.post(self.MAIN_URL + "register/confirm/", self.confirm_data_bad).json()
        self.assertEqual(response['Need all fields'], 'email, token')
