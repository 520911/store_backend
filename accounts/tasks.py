from __future__ import absolute_import

from django.core.mail import EmailMultiAlternatives

from accounts.models import ConfirmEmailToken, User
from shop import settings
from shop.celery import app


@app.task
def send_token_email(user_id):
    instance = User.objects.filter(id=user_id)
    token, _ = ConfirmEmailToken.objects.get_or_create(user=instance)
    msg = EmailMultiAlternatives(
        # title:
        f"Confirm email token {instance.email}",
        # message:
        f"Confirm email token {token.key}",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [instance.email]
    )
    msg.send()
