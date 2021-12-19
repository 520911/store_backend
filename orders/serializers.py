from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserSerializer, ContactsSerializer
from .models import Shop, Order, Product, OrderItem, ProductInfo


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


class ProductInfoSerializer(ModelSerializer):
    shop = ShopSerializer()
    product = ProductsSerializer()

    class Meta:
        model = ProductInfo
        fields = ['model', 'product', 'shop', 'quantity', 'price', 'price_rrc']


class OrderItemSerializer(ModelSerializer):

    order = OrdersSerializer(read_only=True)
    product_info = ProductInfoSerializer()

    class Meta:
        model = OrderItem
        fields = ['order', 'product_info', 'quantity']


class OrderItemAddSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order', 'product_info', 'quantity']
