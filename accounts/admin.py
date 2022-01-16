from django.contrib import admin
from .models import ConfirmEmailToken, User, Contact


admin.site.register(ConfirmEmailToken)
admin.site.register(User)
admin.site.register(Contact)
