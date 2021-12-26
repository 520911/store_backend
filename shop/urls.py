from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar


schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[path('api/v1/', include('shop.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('accounts.urls', 'accounts_api')),
    path('api/v1/', include('orders.urls', 'orders_api')),
    path('api/v1/', include('partners.urls', 'partners_api')),
    path(  # new
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
    path(  # new
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
]
