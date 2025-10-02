from auditlog.registry import auditlog
from django.db import models

from src.report.enums import ReportEnum
from src.user.models import User


class Report(models.Model):
    id = models.BigAutoField(primary_key=True)
    content_id = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ReportEnum.types())
    status = models.CharField(max_length=20, choices=ReportEnum.statuses())
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def is_user(self):
        return self.type == ReportEnum.TYPE_USER.value

    def is_media(self):
        return self.type == ReportEnum.TYPE_MEDIA.value


auditlog.register(Report)
