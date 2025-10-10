from django.core.files.uploadedfile import UploadedFile

from src.media.enums import MediaEnum
from src.media.models import Media
from src.media.services.hashtag.hashtag_service import HashtagService
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import compress_media_task, MEDIA_TYPE_MEDIA
from src.user.models import User, UserProfile


class UploadMediaService:
    def upload_media(self, user: User, uploaded_file: UploadedFile, description: str) -> None:
        local_storage_service = LocalStorageService()
        remote_storage_service = RemoteStorageService()
        hashtag_service = HashtagService()

        # upload to temp local storage
        file_data = local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
        remote_file_name = file_data.get('remote_file_name')
        file_type = file_data.get('file_type')
        remote_file_path = f'{file_type}/media/{user.id}/{remote_file_name}'

        remote_file_info = remote_storage_service.upload_file(
            local_file_type=file_type,
            local_file_path=file_data.get('local_file_path'),
            remote_file_path=remote_file_path
        )

        media = Media.objects.create(
            file_info=remote_file_info,
            file_type=file_data.get('file_type'),
            status=MediaEnum.STATUS_PENDING.value,
            description=description,
            user=user,
        )

        # save hashtags
        hashtag_service.save_hashtags(media=media, description=description)

        # Increase count
        profile:UserProfile = user.profile
        profile.media_count +=1
        profile.save()

        # compress media
        compress_media_task.delay(
            media_id=media.id,
            media_type=MEDIA_TYPE_MEDIA,
            create_thumbnail=True,
            create_trailer=True
        )
