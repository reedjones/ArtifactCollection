__author__ = "reed@reedjones.me"

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile

from rest_framework.authtoken.models import Token
USER = get_user_model()

@receiver(post_save, sender=USER)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a new user is registered."""
    if created:
        UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=get_user_model())
# def save_user_profile(sender, instance, **kwargs):
#     """Save the user profile whenever the user is saved."""
#     # instance.profile.save()
#     print("signal")


@receiver(post_save, sender=USER)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)