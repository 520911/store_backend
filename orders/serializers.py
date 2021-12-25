from rest_framework.fields import SerializerMethodField
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
    full_price = SerializerMethodField()
    full_price_rrc = SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order', 'product_info', 'quantity', 'full_price', 'full_price_rrc']

    def get_full_price(self, value):
        return value.quantity * value.product_info.price

    def get_full_price_rrc(self, value):
        return value.quantity * value.product_info.price_rrc


class OrderItemAddSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product_info', 'quantity']
