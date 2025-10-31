from src.media.enums import MediaEnum
from src.media.models import Media
from src.storage.services.remote_storage_service import RemoteStorageService


class DeleteUserMediaTask:
    def delete_user_media(self, user_id: int):
        remote_storage_service = RemoteStorageService()
        media = Media.objects.filter(user_id=user_id).filter(status=MediaEnum.STATUS_DELETED.value)

        for item in media:
            media_item: Media = item
            remote_storage_service.delete_file(
                file_id=media_item.file_info.get('file_id'),
                file_path=media_item.file_info.get('file_path')
            )

            if media_item.file_thumbnail is not None:
                remote_storage_service.delete_file(
                    file_id=media_item.file_thumbnail.get('file_id'),
                    file_path=media_item.file_thumbnail.get('file_name')
                )

            if media_item.file_trailer is not None:
                remote_storage_service.delete_file(
                    file_id=media_item.file_trailer.get('file_id'),
                    file_path=media_item.file_trailer.get('file_name')
                )

            media_item.delete()
