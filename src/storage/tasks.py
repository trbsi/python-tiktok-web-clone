import bugsnag
from celery import shared_task

from src.storage.crons.clear_temp_folder.clear_temp_folder_task import ClearTempFolderTask
from src.storage.crons.compress_media_task.compress_media_task import CompressMediaTask


@shared_task
def task_compress_media_task(
        media_type: str,
        media_id: int,
        create_thumbnail: bool = False,
        create_trailer: bool = False,
        should_compress_media: bool = True
) -> None:
    try:
        task = CompressMediaTask()
        task.compress_media(
            media_type=media_type,
            media_id=media_id,
            create_thumbnail=create_thumbnail,
            create_trailer=create_trailer,
            should_compress_media=should_compress_media
        )
    except Exception as e:
        bugsnag.notify(e)


@shared_task
def cron_clear_temp_folder():
    try:
        task = ClearTempFolderTask()
        task.clear_temp_folder()
    except Exception as e:
        bugsnag.notify(e)
