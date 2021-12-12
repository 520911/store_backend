from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('accounts.urls', 'accounts_api')),
    path('api/v1/', include('orders.urls', 'orders_api')),
]
