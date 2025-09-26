import logging
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
    log = logging.getLogger('app_logger')

    log.info('# TODO ušao u compress_media_task')
    if media_type == 'inbox':
        media = Message.objects.get(pk=media_id)
    else:
        media = Media.objects.get(pk=media_id)

    print(media.file_info)
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

    log.info('# TODO skinuo sa remote')

    # compress file
    if media.is_image():
        compress_file_service.compress_image(path=local_file_path)
        output_file_path = local_file_path
    else:
        extension = Path(original_file_info.get('file_name')).suffix
        file_name = f'{media.id}_{original_file_info.get('file_id')}.{extension}'
        output_file_path = f'{settings.MEDIA_ROOT}/{file_name}'
        compress_file_service.compress_video(input_path=local_file_path, output_path=output_file_path)

    log.info('# TODO napravio kompresiju')

    # upload to remote and replace
    file_info = remote_storage_service.upload_file(
        local_file_path=output_file_path,
        remote_file_name=original_file_info.get('file_name')
    )

    log.info('# TODO uploadao na remote')

    # update model
    if media_type == 'inbox':
        media.file_info = file_info
        media.save()
    else:
        # TODO save media properly
        media = Media.objects.get(pk=media_id)

    log.info('# spremi model')

    # remove local files
    os.remove(local_file_path_directory)

    log.info('# TODO izbrisao local')
