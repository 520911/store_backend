from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, Contact
from .models import Shop, Category, Order, Product
from .serializers import ShopSerializer, CategoriesSerializer, OrdersSerializer, ProductsSerializer


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
