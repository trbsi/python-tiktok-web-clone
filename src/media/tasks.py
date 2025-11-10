import bugsnag
from celery import shared_task

from src.media.crons.delete_media.delete_media_cron import DeleteMediaCron
from src.media.crons.locked_media.lock_media_cron import LockMediaCron
from src.media.crons.publish_scheduled_media.publish_scheduled_media_cron import PublishScheduledMediaCron
from src.media.crons.recreate_media_asset.recreate_thumbnail_and_trailer_cron import RecreateThumbnailAndTrailerCron
from src.media.crons.scheduled_slots.update_creator_timezone_slots_cron import UpdateCreatorTimezoneSlotsCron


@shared_task
def cron_publish_scheduled_media():
    try:
        task = PublishScheduledMediaCron()
        task.publish_scheduled_media()
    except Exception as e:
        bugsnag.notify(e)


@shared_task
def cron_set_current_publishing_slot():
    try:
        task = UpdateCreatorTimezoneSlotsCron()
        task.update_timezone_slots()
    except Exception as e:
        bugsnag.notify(e)


@shared_task
def cron_lock_media():
    try:
        task = LockMediaCron()
        task.lock_media()
    except Exception as e:
        bugsnag.notify(e)


@shared_task
def cron_recreate_thumbnail_and_trailer():
    try:
        task = RecreateThumbnailAndTrailerCron()
        task.recreate_media_asset()
    except Exception as e:
        bugsnag.notify(e)


@shared_task
def cron_delete_media():
    try:
        service = DeleteMediaCron()
        service.delete_media()
    except Exception as e:
        bugsnag.notify(e)
