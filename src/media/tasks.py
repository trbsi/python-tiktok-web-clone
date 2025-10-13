from celery import shared_task

from src.media.crons.pusblish_scheduled_media.publish_scheduled_media_task import PublishScheduledMediaTask


@shared_task
def publish_scheduled_media():
    task = PublishScheduledMediaTask()
    task.publish_media()
