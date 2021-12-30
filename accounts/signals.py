from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from shop import settings
from .tasks import send_token_email


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        send_token_email.delay(instance.email)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    msg = EmailMultiAlternatives(
        # title:
        f"Confirm email token {reset_password_token.user.email}",
        # message:
        f"Confirm email token {reset_password_token.key}",
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()
