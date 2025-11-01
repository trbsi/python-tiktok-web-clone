from celery import shared_task

from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask


@shared_task
def task_auto_reply(message_id: int, send_message_service):
    task = AutoReplyTask()
    task.auto_reply(message_id, send_message_service)
