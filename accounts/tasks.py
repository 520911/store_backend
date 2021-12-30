from django.core.mail import EmailMultiAlternatives

from accounts.models import ConfirmEmailToken, User
from shop import settings
from shop.celery import app


@app.task
def send_token_email(email):
    user = User.objects.filter(email=email).first()
    token, _ = ConfirmEmailToken.objects.get_or_create(user=user)
    msg = EmailMultiAlternatives(
        # title:
        f"Confirm email token {email}",
        # message:
        f"Confirm email token {token.key}",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [email]
    )
    msg.send()
