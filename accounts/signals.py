from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop import settings
from .models import ConfirmEmailToken
from .tasks import send_token_email


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # send_token_email.delay(instance.pk)

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

# def send_token(email, token, **kwargs):
#     # token, _ = ConfirmEmailToken.objects.get_or_create(user=user)
#     msg = EmailMultiAlternatives(
#         # title:
#         f"Confirm email token {email}",
#         # message:
#         f"Confirm email token {token.key}",
#         # from:
#         settings.EMAIL_HOST_USER,
#         # to:
#         [email]
#     )
#     msg.send()
