from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from orders.serializers import ShopSerializer, OrdersSerializer
from .tasks import upload_partner_price


class PartnerUpdate(APIView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=status.HTTP_403_FORBIDDEN)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                upload_partner_price.delay(url=url, user_id=request.user.id)
                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Need all arguments'})


class ShopStateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=status.HTTP_403_FORBIDDEN)
        user_shop = request.user.shop
        serializer = ShopSerializer(user_shop)
        return JsonResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=status.HTTP_403_FORBIDDEN)
        if {'state'}.issubset(request.data):
            state = request.data.get('state')
            request.user.shop.state = bool(state)
            serializer = ShopSerializer(instance=request.user.shop, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({'Change info successfully': status.HTTP_200_OK})
        else:
            return JsonResponse({'Need all fields': 'state'})


class OrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Only for shops'}, status=status.HTTP_403_FORBIDDEN)
        user_orders = request.user.orders
        serializer = OrdersSerializer(user_orders, many=True)
        return JsonResponse(serializer.data, safe=False)
