import re as regex

from django.core.files.uploadedfile import UploadedFile

from src.media.enums import MediaEnum
from src.media.models import Hashtag, Media
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import compress_media_task


class UploadMediaService:
    def upload(self, uploaded_file: UploadedFile, description: str) -> None:
        local_storage_service = LocalStorageService()
        remote_storage_service = RemoteStorageService()

        # uploade to temp local storage
        file_data = local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
        remote_file_info = remote_storage_service.upload_file(
            local_file_path=file_data.get('local_file_path'),
            remote_file_name=file_data.get('remote_file_name'),
        )

        media = Media.objects.create(
            file_info=remote_file_info,
            file_type=file_data.get('file_type'),
            status=MediaEnum.STATUS_PENDING.value,
            description=description,
        )

        # save hashtags
        self._save_hashtags(media=media, description=description)

        # compress media
        compress_media_task.delay(media=media, create_thumbnail=True, create_trailer=True)

    def _save_hashtags(self, media: Media, description: str) -> None:
        # r"#\w+" → '#' followed by one or more word characters (letters, digits, underscore)
        hashtags = regex.findall(r"#\w+", description)
        if not hashtags:
            return

        hashtag_ids = []
        for hashtag in hashtags:
            hashtag = hashtag.lower()
            record = Hashtag.objects.get_or_create(hashtag=hashtag)
            record.count = record.count + 1
            record.save()
            hashtag_ids.append(record.id)

        media.hashtags.add(*hashtag_ids)
