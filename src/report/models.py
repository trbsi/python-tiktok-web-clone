from auditlog.registry import auditlog
from django.db import models

from src.report.enums import ReportEnum
from src.user.models import User


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    content_id = models.IntegerField()
    type = models.CharField(max_length=20, choices=ReportEnum.types())
    status = models.CharField(max_length=20, choices=ReportEnum.statuses())
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


auditlog.register(Report)
