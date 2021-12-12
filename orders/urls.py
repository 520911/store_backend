from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import ShopListView, CategoriesListView, PartnerUpdate

app_name = 'orders'


urlpatterns = [
    path('shops/', ShopListView.as_view(), name='shop_list'),
    path('categories/', CategoriesListView.as_view(), name='shop_list'),
    path('partner/update/', PartnerUpdate.as_view(), name='update'),
]
