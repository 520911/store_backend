from django.urls import path

from orders.views import ShopListView, CategoriesListView

app_name = 'orders'

urlpatterns = [
    path('shops/', ShopListView.as_view(), name='shop_list'),
    path('categories/', CategoriesListView.as_view(), name='shop_list'),
]
