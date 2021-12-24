from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from ujson import loads as json_loads

from accounts.models import User, Contact
from .models import Shop, Category, Order, Product, OrderItem, ProductInfo
from .serializers import ShopSerializer, CategoriesSerializer, OrdersSerializer, ProductsSerializer, \
    OrderItemAddSerializer, OrderItemSerializer


class ShopListView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.type != 'buyer':
            return JsonResponse({'Status': False, 'Error': 'Только для покупателей'}, status=status.HTTP_403_FORBIDDEN)
        user_orders = request.user.orders
        serializer = OrdersSerializer(user_orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.type != 'buyer':
            return JsonResponse({'Status': False, 'Error': 'Только для покупателей'}, status=status.HTTP_403_FORBIDDEN)
        if {'id', 'contact'}.issubset(request.data):
            user = User.objects.filter(id=request.data['id']).first()
            contact = Contact.objects.filter(id=request.data['contact']).first()
            if user and contact:
                Order.objects.update_or_create(user=user, contact=contact, state='new')
                return Response({'Status': 'OK'})
            else:
                return Response({'Status': 'Такого юзера или контакта не существует'})
        else:
            return Response({'Заполните все данные': 'id, contact'})


class SearchProductsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductsSerializer

    def get_queryset(self):
        query = None
        category_id = self.request.query_params.get('category_id')
        if category_id:
            query = Q(category_id=category_id)
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            query = query & Q(product_infos__shop_id=shop_id)

        queryset = Product.objects.filter(query).select_related('category').prefetch_related('category__shops')
        return queryset


class BasketView(ModelViewSet):
    queryset = OrderItem.objects.filter(order__state='basket').select_related('order')
    serializer_class = OrderItemAddSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order__dt']

    def get_queryset(self):
        user = self.request.user
        orders = OrderItem.objects.filter(order__user=user).select_related('order')
        return orders

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def create_basket(self, request, *args, **kwargs):
        if request.user.type != 'buyer':
            return JsonResponse({'Status': False, 'Error': 'Только для покупателей'}, status=status.HTTP_403_FORBIDDEN)
        items = request.data.get('items')
        if items:
            try:
                items_list = json_loads(items)
            except ValueError:
                return Response({'Status': False, 'Error': 'Неверный формат данных'})
            else:
                order, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                for item in items_list:
                    try:
                        product_info = ProductInfo.objects.filter(id=item['product_info']).first()
                    except KeyError:
                        return Response({'Status': 'Ошибка в поле product_info'})
                    if product_info:
                        try:
                            OrderItem.objects.update_or_create(order_id=order.id,
                                                               product_info_id=product_info.id,
                                                               quantity=item['quantity'])
                        except (IntegrityError, KeyError) as errors:
                            return Response({'Status': f'{errors}'})
                    else:
                        return Response({'Такого товара не существует'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Status': 'OK'})
        else:
            return Response({'Заполните все данные': 'items'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_basket(self, request, *args, **kwargs):
        if request.user.type != 'buyer':
            return JsonResponse({'Status': False, 'Error': 'Только для покупателей'}, status=status.HTTP_403_FORBIDDEN)
        items = request.data.get('items')
        if items:
            try:
                items_list = json_loads(items)
            except ValueError:
                return Response({'Status': False, 'Error': 'Неверный формат данных'})
            else:
                for item in items_list:
                    try:
                        product_info = ProductInfo.objects.filter(id=item['product_info']).first()
                    except KeyError:
                        return Response({'Status': 'Ошибка в поле product_info'})
                    if product_info:
                        try:
                            OrderItem.objects.filter(product_info=product_info).update(quantity=item['quantity'])
                        except KeyError as errors:
                            return Response({'Status': f'{errors}'})
                    else:
                        return Response({'Такого товара не существует'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Status': 'OK'})
        else:
            return Response({'Заполните все данные': 'items'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['destroy'])
    def delete_basket(self, request, *args, **kwargs):
        if request.user.type != 'buyer':
            return JsonResponse({'Status': False, 'Error': 'Только для покупателей'}, status=status.HTTP_403_FORBIDDEN)
        items = request.data.get('items')
        if items:
            for item in request.data['items'].split(','):
                try:
                    product_info = ProductInfo.objects.filter(id=item).first()
                except KeyError:
                    return Response({'Status': 'Ошибка в поле product_info'})
                if product_info:
                    order_item = OrderItem.objects.filter(product_info=product_info)
                    self.perform_destroy(order_item)
                else:
                    return Response({'Такого товара не существует'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Status': 'OK'})
        else:
            return Response({'Заполните все данные': 'items'}, status=status.HTTP_400_BAD_REQUEST)
