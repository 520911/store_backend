import pytest
from django.urls import reverse
from rest_framework import status

from accounts.models import User, Contact


def test_dummy():
    assert True


@pytest.mark.django_db
def test_get_contact(client, contact_factory):
    user = User.objects.create(
        first_name='denis',
        last_name='denis',
        email='denis@denis.ru',
        password='123',
        company='it',
        position='it'
    )
    main_url = 'http://127.0.0.1:8000/api/v1/user/contact/'
    # url = reverse('register/')
    contact = {
        'user': user, 'city': 'city', 'street': 'street'
    }
    response = client.post(main_url, data=contact)
    assert response.status_code == status.HTTP_201_CREATED
