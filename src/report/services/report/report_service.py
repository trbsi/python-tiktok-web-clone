from django.contrib.auth.models import AnonymousUser

from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.report.enums import ReportEnum
from src.report.models import Report
from src.user.models import User


class ReportService:
    def report(self, type: str, content_id: int, user: AnonymousUser | User) -> None:
        reported_by = user
        if not user.is_authenticated:
            reported_by = None

        Report.objects.create(
            type=type,
            content_id=content_id,
            reported_by=reported_by,
            status=ReportEnum.STATUS_PENDING.value
        )

        admin_email = EmailValueObject(
            subject='Content Reported!',
            template_path='emails/admin/content_reported.html',
            template_variables={'type': type, 'reported_by': reported_by, 'id': content_id},
            to=['admins']
        )
        NotificationService.send_notification(admin_email)
