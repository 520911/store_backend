from django.urls import path
from .views import PartnerUpdate

app_name = 'partners'

urlpatterns = [
    path('partner/update/', PartnerUpdate.as_view(), name='update'),
]
