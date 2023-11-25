__author__ = "reed@reedjones.me"

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add your custom fields here

    def __str__(self):
        return self.username


class UserProfileManager(models.Manager):
    def get_active_profiles(self):
        return self.filter(user__is_active=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add additional fields as needed
    objects = UserProfileManager()
    receive_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# @receiver(post_save, sender=YourModel)
# def create_notification(sender, instance, created, **kwargs):
#     if created:
#         user = instance.user  # Adjust this based on your model structure
#         message = "New item created: {}".format(instance.name)  # Customize the message
#         Notification.objects.create(user=user, message=message)