from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from app.utils import reverse_lazy_admin
from src.media.models import Media
from src.report.models import Report
from src.user.models import User


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('content_id', 'status', 'type', 'created_at')
    fields = (
        'content_id',
        'description',
        'type',
        'status',
        'reported_by',
        'get_content',
    )
    readonly_fields = ('get_content',)

    @admin.display(description="Content")
    def get_content(self, report: Report):
        if report.is_user():
            user = User.objects.get(id=report.content_id)
            href = reverse_lazy('user.profile', kwargs={'username': user.username})
            return format_html(f'<a href="{href}">View user</a>', )

        if report.is_media():
            media: Media = Media.objects.get(id=report.content_id)
            media_url = media.get_file_url()
            if media.is_image():
                return format_html(f'<img src="{media_url}">')
            if media.is_video():
                admin_media_url = reverse_lazy_admin(object=media, action='change', args=(media.id,))

                return format_html(
                    f'<div><a hre="{admin_media_url}" > View media </a></div>'
                    f' <div> <video controls><source src="{media_url}" type = "video/mp4"></video></div>')
        return ''
