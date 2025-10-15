from celery import shared_task

from src.media.crons.publish_scheduled_media.publish_scheduled_media_task import PublishScheduledMediaTask
from src.media.crons.scheduled_slots.update_creator_timezone_slots_task import UpdateCreatorTimezoneSlotsTask


@shared_task
def publish_scheduled_media():
    task = PublishScheduledMediaTask()
    task.publish_scheduled_media()


@shared_task
def set_current_publishing_slot():
    task = UpdateCreatorTimezoneSlotsTask()
    task.update_timezone_slots()
