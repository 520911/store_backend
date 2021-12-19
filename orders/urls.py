from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from orders.views import ShopListView, CategoriesListView, OrderView, SearchProductsView, BasketView

app_name = 'orders'

basket_methods = BasketView.as_view({
    'get': 'list',
    'post': 'create_basket',
    # 'put': 'contact_update',
    # 'delete': 'contact_delete'
})

url_contacts = format_suffix_patterns([
    path('basket/', basket_methods, name='basket_api'),
])

urlpatterns = [
                  path('shops/', ShopListView.as_view(), name='shop_list'),
                  path('categories/', CategoriesListView.as_view(), name='shop_list'),
                  path('order/', OrderView.as_view(), name='shop_orders'),
                  path('products', SearchProductsView.as_view(), name='search_products'),
              ] + url_contacts
