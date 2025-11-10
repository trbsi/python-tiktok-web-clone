import uuid
from pathlib import Path

from src.core.utils import remote_file_path_for_conversation, remote_file_path_for_media
from src.inbox.models import Message
from src.media.models import Media
from src.storage.services.media_manipulation.compress_file_service import CompressFileService
from src.storage.services.remote_storage_service import RemoteStorageService


class CompressMediaService:
    def handle_compression(
            self,
            media: Media | Message,
            local_file_type: str,
            local_file_path: str,
            local_file_path_directory: str
    ) -> dict:
        remote_storage_service = RemoteStorageService()
        compress_file_service = CompressFileService()

        original_file_info = media.file_info
        extension = Path(original_file_info.get('file_path')).suffix  # example: .jpg or .mp4
        new_file_name = f'{media.__class__.__name__}_{media.id}_media_{uuid.uuid4()}{extension}'

        if isinstance(media, Message):
            new_file_path = remote_file_path_for_conversation(media.conversation, new_file_name)
        elif isinstance(media, Media):
            new_file_path = remote_file_path_for_media(media, new_file_name)

        # compress file
        if media.is_image():
            compress_file_service.compress_image(path=local_file_path)
            output_compressed_file_path = local_file_path
        elif media.is_video():
            output_compressed_file_path = f'{local_file_path_directory}/{new_file_name}'
            compress_file_service.compress_video(
                input_path=local_file_path,
                output_path=output_compressed_file_path
            )
        else:
            raise Exception('Unknown media type')

        # upload to remote and replace
        file_info = remote_storage_service.upload_file(
            local_file_type=local_file_type,
            local_file_path=output_compressed_file_path,
            remote_file_path=new_file_path
        )

        # update model
        media.file_info = file_info
        media.save()

        # remove remote file
        remote_storage_service.delete_file(
            file_id=original_file_info.get('file_id'),
            file_path=original_file_info.get('file_path')
        )

        return {
            'output_compressed_file_path': output_compressed_file_path,
        }
