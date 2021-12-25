from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop import settings
from .models import ConfirmEmailToken


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = ConfirmEmailToken.objects.create(user=instance)
        msg = EmailMultiAlternatives(
            # title:
            f"Confirm email token {instance.email}",
            # message:
            f"Confirm email token {token.key}",
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            instance.email
        )
        msg.send()
