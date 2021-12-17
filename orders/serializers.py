from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer, ContactsSerializer
from .models import Shop, Order, Product


class ShopSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Shop
        fields = ['name', 'url', 'state', 'user']


class CategoriesSerializer(ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = Shop
        fields = ['name', 'shops']


class OrdersSerializer(ModelSerializer):
    user = UserSerializer()
    contact = ContactsSerializer()

    class Meta:
        model = Order
        fields = ['user', 'dt', 'state', 'contact']


class ProductsSerializer(ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Product
        fields = ['name', 'category']
