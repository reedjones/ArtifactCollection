__author__ = "reed@reedjones.me"


import datetime as dt
from http import HTTPStatus

from django.test import Client, override_settings, TestCase
from django.utils import timezone

from core.models import WebhookMessage


@override_settings(WEBHOOK_TOKEN="abc123")
class GithubWebhookTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_bad_method(self):
        response = self.client.get("/webhooks/github/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/")

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_missing_token(self):
        response = self.client.post(
            "/webhooks/github/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert (
            response.content.decode() == "Incorrect token in Acme-Webhook-Token header."
        )

    def test_bad_token(self):
        response = self.client.post(
            "/webhooks/github/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
            HTTP_ACME_WEBHOOK_TOKEN="def456",
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert (
            response.content.decode() == "Incorrect token in Github-Webhook-Token header."
        )

    def test_success(self):
        start = timezone.now()
        old_message = WebhookMessage.objects.create(
            received_at=start - dt.timedelta(days=100),
        )

        response = self.client.post(
            "/webhooks/github/mPnBRC1qxapOAxQpWmjy4NofbgxCmXSj/",
            HTTP_ACME_WEBHOOK_TOKEN="abc123",
            content_type="application/json",
            data={"this": "is a message"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.content.decode() == "Message received okay."
        assert not WebhookMessage.objects.filter(id=old_message.id).exists()
        awm = WebhookMessage.objects.get()
        assert awm.received_at >= start
        assert awm.payload == {"this": "is a message"}