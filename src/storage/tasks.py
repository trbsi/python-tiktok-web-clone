import bugsnag
from celery import shared_task

from src.storage.crons.clear_temp_folder.clear_temp_folder_cron import ClearTempFolderCron
from src.storage.crons.compress_media_task.process_media_task import ProcessMediaTask


@shared_task
def task_process_media(
        media_type: str,
        media_id: int,
        create_thumbnail: bool = False,
        create_trailer: bool = False,
        should_compress_media: bool = False
) -> None:
    try:
        task = ProcessMediaTask()
        task.process_media(
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
        task = ClearTempFolderCron()
        task.clear_temp_folder()
    except Exception as e:
        bugsnag.notify(e)
