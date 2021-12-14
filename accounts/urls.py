from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework.urlpatterns import format_suffix_patterns

from accounts.views import RegisterUserView, ConfirmRegisterUserView, UserLoginView, ContactsView, UserDetailsView

app_name = 'accounts'

contacts_methods = ContactsView.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'contact_update',
    'delete': 'contact_delete'
})

url_contacts = format_suffix_patterns([
    path('contact/', contacts_methods, name='contacts_api'),
])

urlpatterns = [
                  path('register/', RegisterUserView.as_view(), name='register'),
                  path('register/confirm/', ConfirmRegisterUserView.as_view(), name='register_confirm'),
                  path('login/', UserLoginView.as_view(), name='login'),
                  path('details/', UserDetailsView.as_view(), name='user_details'),
                  path('password_reset/', reset_password_request_token, name='password_reset'),
                  path('password_reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
              ] + url_contacts
