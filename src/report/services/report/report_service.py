from django.contrib.auth.models import AnonymousUser

from src.media.models import Media
from src.notification.services.notification_service import NotificationService
from src.notification.value_objects.email_value_object import EmailValueObject
from src.report.enums import ReportEnum
from src.report.models import Report
from src.user.models import User


class ReportService:
    def report(self, type: str, content_id: int, description: str, user: AnonymousUser | User) -> None:
        if user.is_authenticated:
            reported_by = user
            reported_by_username = user.username
        else:
            reported_by = None
            reported_by_username = 'guest'

        if type == ReportEnum.TYPE_USER.value:
            content_object = User.objects.get(id=content_id)
        elif type == ReportEnum.TYPE_MEDIA.value:
            content_object = Media.objects.get(id=content_id)

        Report.objects.create(
            content_object=content_object,
            description=description,
            reported_by=reported_by,
            status=ReportEnum.STATUS_PENDING.value
        )

        template_vars = {
            'type': type,
            'reported_by': reported_by_username,
            'id': content_id,
            'description': description,
        }

        admin_email = EmailValueObject(
            subject='Content Reported!',
            template_path='emails/admin/content_reported.html',
            template_variables=template_vars,
            to=['admins']
        )
        NotificationService.send_notification(admin_email)
