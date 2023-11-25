__author__ = "reed@reedjones.me"
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Custom logic to save the user instance.
        In this case, we'll create an email confirmation record.
        """
        user = super().save_user(request, user, form, commit=False)
        user.is_active = False  # Deactivate the user until email confirmation
        user.save()

        email_address = user.emailaddress_set.create(
            email=user.email,
            primary=True,
            verified=False,
        )

        confirmation = EmailConfirmation.create(email_address)
        confirmation.sent = False
        confirmation.save()

        return user

    def is_open_for_signup(self, request):
        """
        Checks whether signups are allowed.
        By default, this method returns True.
        You can customize it based on your requirements.
        """
        return True

    def respond_email_verification_sent(self, request, user):
        """
        Custom logic for responding to a verification email sent.
        This method is called after the email confirmation is sent.
        """

        current_site = get_current_site(request)
        email_subject = 'Confirm your email'
        email_body = f'Click the following link to confirm your email: {reverse("account_confirm_email", args=[user.id, EmailConfirmationHMAC.from_user(user).key])}'
        send_mail(email_subject, email_body, 'from@example.com', [user.email])
        pass  # You can add custom logic if needed




    def respond_email_confirmation(self, request, confirmation):
        """
        Custom logic for responding to email confirmation.
        This method is called after the user clicks the confirmation link.
        """
        redirect_url = '/'  # Redirect to a specific URL after confirmation
        return redirect_url