from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer
from .models import Shop


class ShopSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Shop
        fields = ['name', 'url', 'state', 'user']


class CategoriesSerializer(ModelSerializer):
    shops = ShopSerializer()

    class Meta:
        model = Shop
        fields = ['name', 'shops']
