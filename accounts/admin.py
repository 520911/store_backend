from django.contrib import admin
from .models import ConfirmEmailToken, User


admin.site.register(ConfirmEmailToken)
admin.site.register(User)
