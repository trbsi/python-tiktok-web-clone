import json

import bugsnag
from pywebpush import webpush

from app import settings
from src.notification.models import WebPushSubscription
from src.notification.value_objects.push_notification_value_object import PushNotificationValueObject


class BrowserService:
    @staticmethod
    def send(notification: PushNotificationValueObject) -> None:
        if notification.user_id is None:
            return

        web_push_notification = WebPushSubscription.objects.filter(user_id=notification.user_id).first()
        if web_push_notification is None:
            return

        try:
            payload = {
                "title": notification.title,
                "body": notification.body,
                "url": notification.url
            }
            claims = {
                "sub": settings.WEB_PUSH_SUBJECT
            }
            webpush(
                subscription_info=web_push_notification.subscription,
                data=json.dumps(payload),
                vapid_private_key=settings.WEB_PUSH_PRIVATE_KEY,
                vapid_claims=claims,
            )
        except Exception as e:
            bugsnag.notify(e)
