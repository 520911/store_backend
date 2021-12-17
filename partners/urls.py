from django.urls import path
from .views import PartnerUpdate, ShopStateView, OrdersView

app_name = 'partners'

urlpatterns = [
    path('partner/update/', PartnerUpdate.as_view(), name='update_price'),
    path('partner/state/', ShopStateView.as_view(), name='shop_state'),
    path('partner/ordres/', OrdersView.as_view(), name='orders'),
]
