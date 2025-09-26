import os
from pathlib import Path

from celery import shared_task

from app import settings
from src.inbox.models import Message
from src.media.models import Media
from src.storage.services.compress_file_service import CompressFileService
from src.storage.services.remote_storage_service import RemoteStorageService


@shared_task
def compress_media_task(media_type: str, media_id: int) -> None:
    if media_type == 'inbox':
        media = Message.objects.get(pk=media_id)
    else:
        media = Media.objects.get(pk=media_id)

    if media.file_info is None:
        return

    remote_storage_service = RemoteStorageService()
    compress_file_service = CompressFileService()
    original_file_info = media.file_info
    local_file_path_directory = os.path.join(settings.MEDIA_ROOT, 'temp')

    # download file from remote
    local_file_path = remote_storage_service.download_file(
        file_id=original_file_info.get('file_id'),
        file_name=original_file_info.get('file_name'),
        local_file_path_directory=local_file_path_directory
    )

    # compress file
    if media.is_image():
        compress_file_service.compress_image(path=local_file_path)
        output_file_path = local_file_path
    elif media.is_video():
        extension = Path(original_file_info.get('file_name')).suffix  # example: .jpg or .mp4
        file_name = f'{media.id}_{original_file_info.get('file_id')}{extension}'
        output_file_path = f'{local_file_path_directory}/{file_name}'
        compress_file_service.compress_video(input_path=local_file_path, output_path=output_file_path)
    else:
        raise Exception('Unknown media type')

    # upload to remote and replace
    file_info = remote_storage_service.upload_file(
        local_file_path=output_file_path,
        remote_file_name=original_file_info.get('file_name')
    )

    # update model
    if media_type == 'inbox':
        media.file_info = file_info
        media.save()
    else:
        # TODO save media properly
        media = Media.objects.get(pk=media_id)

    # remove local files
    os.remove(local_file_path)
