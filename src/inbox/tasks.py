import bugsnag
from celery import shared_task

from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask


@shared_task()
def task_auto_reply(message_id: int):
    try:
        task = AutoReplyTask()
        task.auto_reply(message_id)
    except Exception as e:
        bugsnag.notify(e)
