import os

from app import settings
from src.inbox.models import Message
from src.media.models import Media
from src.storage.services.media_manipulation.compress_media_service import CompressMediaService
from src.storage.services.media_manipulation.thumbnail_service import ThumbnailService
from src.storage.services.media_manipulation.trailer_service import TrailerService
from src.storage.services.remote_storage_service import RemoteStorageService


class CompressMediaTask:
    MEDIA_TYPE_MEDIA = 'media'
    MEDIA_TYPE_INBOX = 'inbox'

    def compress_media(
            self,
            media_type: str,
            media_id: int,
            create_thumbnail: bool = False,
            create_trailer: bool = False
    ) -> None:
        if media_type == self.MEDIA_TYPE_INBOX:
            media = Message.objects.get(id=media_id)
        elif media_type == self.MEDIA_TYPE_MEDIA:
            media = Media.objects.get(id=media_id)

        if media.file_info is None:
            return

        remote_storage_service = RemoteStorageService()
        compress_service = CompressMediaService()
        thumbnail_service = ThumbnailService()
        trailer_service = TrailerService()

        local_file_path_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')
        files_to_remove = []

        # download file from remote
        downloaded_local_file_path = remote_storage_service.download_file(
            file_id=media.file_info.get('file_id'),
            file_path=media.file_info.get('file_path'),
            local_file_path_directory=local_file_path_directory
        )

        # compress file
        compression_result = compress_service.handle_compression(
            media=media,
            local_file_type=media.file_type,
            local_file_path=downloaded_local_file_path,
            local_file_path_directory=local_file_path_directory
        )
        output_compressed_file_path = compression_result.get('output_compressed_file_path')

        # create thumbnail
        if create_thumbnail and media.is_video():
            thumbnail_result = thumbnail_service.snap_thumbnail(
                media=media,
                local_file_type=media.file_type,
                local_file_path=output_compressed_file_path,
                local_file_path_directory=local_file_path_directory,
            )
            files_to_remove.append(thumbnail_result.get('output_thumbnail_path'))

        # create trailer
        if create_trailer and media.is_video():
            trailer_result = trailer_service.make_trailer(
                media=media,
                local_file_type=media.file_type,
                local_file_path=output_compressed_file_path,
                local_file_path_directory=local_file_path_directory,
            )
            files_to_remove.append(trailer_result.get('output_trailer_file_path'))
            files_to_remove = files_to_remove + trailer_result.get('parts')

        # remove local files
        files_to_remove.append(output_compressed_file_path)
        files_to_remove.append(downloaded_local_file_path)
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

        # set model as ready
        if isinstance(media, Media):
            media.is_processed = True
            media.save()
