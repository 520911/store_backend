from rest_framework.generics import ListAPIView

from .models import Shop, Category
from .serializers import ShopSerializer, CategoriesSerializer


class ShopListView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
