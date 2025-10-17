from celery import shared_task

from src.storage.crons.compress_media_task.compress_media_task import CompressMediaTask


@shared_task
def compress_media_task(
        media_type: str,
        media_id: int,
        create_thumbnail: bool = False,
        create_trailer: bool = False
) -> None:
    task = CompressMediaTask()
    task.compress_media(
        media_type=media_type,
        media_id=media_id,
        create_thumbnail=create_thumbnail,
        create_trailer=create_trailer
    )
