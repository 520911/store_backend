from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from accounts.views import RegisterUserView, ConfirmRegisterUserView, UserLoginView, ContactsView, UserDetailsView

app_name = 'accounts'

router = DefaultRouter()
router.register('contact', ContactsView)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register/confirm/', ConfirmRegisterUserView.as_view(), name='register_confirm'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('details/', UserDetailsView.as_view(), name='user_details'),
    path('password_reset/', reset_password_request_token, name='password_reset'),
    path('password_reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
    path('', include(router.urls)),
]
