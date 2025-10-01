from src.notification.services.browser_service import BrowserService
from src.notification.services.email_service import EmailService
from src.notification.value_objects.browser_value_object import BrowserValueObject
from src.notification.value_objects.email_value_object import EmailValueObject


class NotificationService():
    @staticmethod
    def send_notification(*notifications) -> None:
        email_service = EmailService()
        browser_service = BrowserService()

        for notification in notifications:
            if isinstance(notification, EmailValueObject):
                email_service.send(notification)
            if isinstance(notification, BrowserValueObject):
                browser_service.send(notification)
