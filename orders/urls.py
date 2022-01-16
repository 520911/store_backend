from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import ShopListView, CategoriesListView, OrderView, SearchProductsView, BasketView

app_name = 'orders'

# basket_methods = BasketView.as_view({
#     'get': 'list',
#     'post': 'create_basket',
#     'put': 'update_basket',
#     'delete': 'delete_basket'
# })
#
# url_contacts = format_suffix_patterns([
#     path('basket/', basket_methods, name='basket_api'),
# ])

router = DefaultRouter()
router.register('basket', BasketView, basename='baskets')

urlpatterns = [
    path('shops/', ShopListView.as_view(), name='shop_list'),
    path('categories/', CategoriesListView.as_view(), name='shop_list'),
    path('order/', OrderView.as_view(), name='shop_orders'),
    path('products', SearchProductsView.as_view(), name='search_products'),
    path('', include(router.urls)),
]
