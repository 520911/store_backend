from django.urls import path

from orders.views import ShopListView, CategoriesListView, OrderView, SearchProductsView

app_name = 'orders'

urlpatterns = [
    path('shops/', ShopListView.as_view(), name='shop_list'),
    path('categories/', CategoriesListView.as_view(), name='shop_list'),
    path('order/', OrderView.as_view(), name='shop_orders'),
    path('products', SearchProductsView.as_view(), name='search_products'),
]
