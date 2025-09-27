import os
import uuid
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
    extension = Path(original_file_info.get('file_name')).suffix  # example: .jpg or .mp4
    new_file_name = f'{media_type}_{media_id}_{uuid.uuid4()}{extension}'
    local_file_path_directory = os.path.join(settings.MEDIA_ROOT, 'temp')
    files_to_remove = []

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
        output_file_path = f'{local_file_path_directory}/{new_file_name}'
        compress_file_service.compress_video(input_path=local_file_path, output_path=output_file_path)
    else:
        raise Exception('Unknown media type')

    # upload to remote and replace
    file_info = remote_storage_service.upload_file(
        local_file_path=output_file_path,
        remote_file_name=new_file_name
    )

    files_to_remove.append(output_file_path)
    files_to_remove.append(local_file_path)

    # update model
    if media_type == 'inbox':
        media.file_info = file_info
        media.save()
    else:
        # TODO save media properly
        media = Media.objects.get(pk=media_id)

    # remove local files
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

    # remove remote file
    remote_storage_service.delete_file(
        file_id=original_file_info.get('file_id'),
        file_name=original_file_info.get('file_name')
    )
