__author__ = "reed@reedjones.me"
import os
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
DEPLOYMENT_EMAILS = os.environ.get("DEPLOYMENT_EMAIL", None)


class Command(BaseCommand):
    help = 'Send deployment notification email'

    def handle(self, *args, **options):
        if not DEPLOYMENT_EMAILS:
            self.stdout.write("No emails to notify\n to add you must set the environment variable DEPLOYMENT_EMAILS "
                              "to comma seperated list containing the emails")

        subject = 'Deployment Notification'
        message = 'A deployment has been made to the server.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = DEPLOYMENT_EMAILS.split(",")

        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        self.stdout.write(self.style.SUCCESS('Deployment notification email sent successfully.'))
