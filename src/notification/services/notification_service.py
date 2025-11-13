from src.notification.services.browser_service import BrowserService
from src.notification.services.email_service import EmailService
from src.notification.services.slack_service import SlackService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.notification.value_objects.push_notification_value_object import PushNotificationValueObject


class NotificationService():
    @staticmethod
    def send_notification(*notifications) -> None:
        email_service = EmailService()
        browser_service = BrowserService()
        slack_service = SlackService()

        for notification in notifications:
            if isinstance(notification, EmailValueObject):
                email_service.send(notification)
            if isinstance(notification, PushNotificationValueObject):
                browser_service.send(notification)
                slack_service.send(notification)
