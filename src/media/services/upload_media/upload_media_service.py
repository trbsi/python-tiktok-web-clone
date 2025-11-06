from django.core.files.uploadedfile import UploadedFile
from django.db import transaction
from django.utils import timezone

from src.media.enums import MediaEnum
from src.media.models import Media, MediaScheduler
from src.media.services.hashtag.hashtag_service import HashtagService
from src.storage.crons.compress_media_task.compress_media_task import CompressMediaTask
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import task_compress_media_task
from src.user.models import User, UserProfile


class UploadMediaService:
    def __init__(
            self,
            remote_storage_service: RemoteStorageService | None = None,
            local_storage_service: LocalStorageService | None = None,
            hashtag_service: HashtagService | None = None,
    ):
        self.remote_storage_service = remote_storage_service or RemoteStorageService()
        self.local_storage_service = local_storage_service or LocalStorageService()
        self.hashtag_service = hashtag_service or HashtagService()

    def upload_media(
            self,
            user: User,
            uploaded_file: UploadedFile,
            description: str,
            post_type: str
    ) -> None:
        """
        post_type: post_now|schedule
        """

        # upload to temp local storage
        file_data = self.local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
        remote_file_name = file_data.get('remote_file_name')
        file_type = file_data.get('file_type')
        remote_file_path = f'{file_type}/media/{user.id}/{remote_file_name}'

        remote_file_info = self.remote_storage_service.upload_file(
            local_file_type=file_type,
            local_file_path=file_data.get('local_file_path'),
            remote_file_path=remote_file_path
        )

        match post_type:
            case 'post_now':
                status = MediaEnum.STATUS_PENDING.value
            case 'schedule':
                status = MediaEnum.STATUS_SCHEDULE.value
            case _:
                status = MediaEnum.STATUS_PENDING.value

        media = Media.objects.create(
            file_info=remote_file_info,
            file_type=file_data.get('file_type'),
            status=status.value,
            description=description,
            user=user,
        )

        profile: UserProfile = user.profile

        # Update media scheduler
        media_scheduler: MediaScheduler
        media_scheduler, created = MediaScheduler.objects.get_or_create(
            user=user,
            defaults={'timezone': 'UTC'}
        )
        if status.is_schedule_status():
            media_scheduler.number_of_scheduled_media += 1
        media_scheduler.timezone = 'UTC' if profile.timezone is None else profile.timezone
        media_scheduler.last_published_at = timezone.now()
        media_scheduler.save()

        # save hashtags
        self.hashtag_service.save_hashtags(media=media, description=description)

        # Increase count
        profile.media_count += 1
        profile.save()

        # compress media
        transaction.on_commit(
            lambda:
            task_compress_media_task.delay(
                media_id=media.id,
                media_type=CompressMediaTask.MEDIA_TYPE_MEDIA,
                create_thumbnail=True,
                create_trailer=True
            )
        )
