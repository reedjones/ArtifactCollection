import datetime as dt
import json
from secrets import compare_digest

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from core.forms import UserProfileForm
from .models import WebhookMessage


@login_required
def view_profile(request):
    # View user profile details
    return render(request, 'profile/view_profile.html')


@login_required
def edit_profile(request):
    # Edit user profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    # Change user password
    # Implement password change logic here
    return render(request, 'registration/change_password.html')


@csrf_exempt
@require_POST
@non_atomic_requests
def listen_webhook(request):
    given_token = request.headers.get("Acme-Webhook-Token", "")
    if not compare_digest(given_token, settings.ACME_WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Acme-Webhook-Token header.",
            content_type="text/plain",
        )

    WebhookMessage.objects.filter(
        received_at__lte=timezone.now() - dt.timedelta(days=7)
    ).delete()
    payload = json.loads(request.body)
    WebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    process_webhook_payload(payload)
    return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    pass


from rest_framework import serializers, status
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupSerializer(serializers.ModelSerializer):
    """override create method to change the password into hash."""

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['username', 'password']


class SignupAPIView(APIView):
    """This api will handle signup"""

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            """If the validation success, it will created a new user."""
            serializer.save()
            res = {'status': status.HTTP_201_CREATED}
            return Response(res, status=status.HTTP_201_CREATED)

        res = {'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """This api will handle login and return token for authenticate user."""

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                """We are reterving the token for authenticated user."""
                token = Token.objects.get(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {
                        "Token": token.key
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
