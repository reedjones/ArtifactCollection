__author__ = "reed@reedjones.me"
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Send deployment notification email'

    def handle(self, *args, **options):
        print("Hey there you...")