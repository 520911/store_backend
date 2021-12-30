from django.db.models.signals import post_save
from django.dispatch import receiver

from shop import settings
from .tasks import send_token_email


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        send_token_email.delay(instance.email)
