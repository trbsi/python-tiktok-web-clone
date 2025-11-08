from django.db.models import Q

from src.media.enums import MediaEnum
from src.media.models import Media
from src.storage.crons.compress_media_task.compress_media_task import CompressMediaTask
from src.storage.tasks import task_compress_media_task


class RecreateThumbnailAndTrailerTask:
    def recreate_media_asset(self):
        media = (
            Media.objects
            .filter(file_type=MediaEnum.FILE_TYPE_VIDEO.value)
            .filter(Q(file_thumbnail__isnull=True) | Q(file_trailer__isnull=True))
        )

        for single_media in media:
            task_compress_media_task.delay(
                media_id=media.id,
                media_type=CompressMediaTask.MEDIA_TYPE_MEDIA,
                create_thumbnail=True if single_media.file_thumbnail is None else False,
                create_trailer=True if single_media.file_trailer is None else False,
                should_compress_media=False,
            )
