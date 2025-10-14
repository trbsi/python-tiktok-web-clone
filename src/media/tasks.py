from celery import shared_task

from src.media.crons.publish_scheduled_media.publish_scheduled_media_task import PublishScheduledMediaTask


@shared_task
def publish_scheduled_media():
    task = PublishScheduledMediaTask()
    task.publish_media()


@shared_task
def set_current_publishing_slot():
    task = PublishScheduledMediaTask()
    task.publish_media()
