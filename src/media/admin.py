from django.contrib import admin, messages
from django.http import HttpRequest
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import action

from src.media.enums import MediaEnum
from src.media.models import Media


@admin.register(Media)
class AdminMedia(ModelAdmin):
    list_filter = ['created_at', 'status']
    list_display = ('id', 'user', 'file_type', 'status', 'created_at')
    fields = (
        'user',
        'file_type',
        'status',
        'description',
        'is_processed',
        'file',
        'trailer',
        'thumbnail',
    )
    readonly_fields = ('created_at', 'file', 'trailer', 'thumbnail')
    search_fields = ('user__username',)

    actions_submit_line = ["mark_as_deleted"]

    @admin.display(description="File")
    def file(self, media: Media) -> str | None:
        if media.is_image():
            return format_html(
                f'<img src="{media.get_file_url()}">'
            )
        if media.is_video():
            return format_html(
                f'<video controls><source src="{media.get_file_url()}"></video>'
            )

        return None

    @admin.display(description="Thumbnail")
    def thumbnail(self, media: Media) -> str | None:
        if media.file_thumbnail is None:
            return None

        return format_html(
            f'<img src="{media.get_thumbnail_url()}">'
        )

    @admin.display(description="Trailer")
    def trailer(self, media: Media) -> str | None:
        if media.file_trailer is None:
            return None

        return format_html(
            f'<video controls><source src="{media.get_trailer_url()}"></video>'
        )

    @action(description="Mark as deleted", )
    def mark_as_deleted(self, request: HttpRequest, media: Media):
        media.status = MediaEnum.STATUS_DELETED.value
        media.save()
        messages.success(request, "Media deleted")

    # def delete_media(self, request: HttpRequest, media_id: int) -> HttpResponse:
    #
    #     return redirect(reverse_lazy_admin(media, 'change', [media_id]))
