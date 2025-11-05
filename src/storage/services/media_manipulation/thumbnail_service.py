import subprocess
import uuid

from src.core.utils import remote_file_path_for_media
from src.media.models import Media
from src.storage.services.remote_storage_service import RemoteStorageService


class ThumbnailService:
    """
    Generate one thumbnail by snapping picture at 10th second
    """

    def snap_thumbnail(
            self,
            media: Media,
            local_file_type: str,
            local_file_path: str,
            local_file_path_directory: str,
            time_in_seconds: int = 10
    ) -> dict:
        output_thumbnail_path = f'{local_file_path_directory}/{uuid.uuid4()}.jpg'
        remote_storage_service = RemoteStorageService()
        command = [
            'ffmpeg',
            '-ss', time_in_seconds,
            '-i', local_file_path,
            '-frames:v', '1',
            '-q:v', '2',
            output_thumbnail_path
        ]
        subprocess.run(command, check=True)

        remote_file_name = f'{media.__class__.__name__}_{media.id}_thumbnail_{uuid.uuid4()}.jpg'
        remote_file_path = remote_file_path_for_media(media, remote_file_name)

        file_info = remote_storage_service.upload_file(
            local_file_type=local_file_type,
            local_file_path=output_thumbnail_path,
            remote_file_path=remote_file_path,
        )

        media.file_thumbnail = file_info
        media.save()

        return {
            'output_thumbnail_path': output_thumbnail_path
        }
