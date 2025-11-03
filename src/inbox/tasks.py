from celery import shared_task

from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask


@shared_task(name='task_auto_reply')
def task_auto_reply(message_id: int):
    task = AutoReplyTask()
    task.auto_reply(message_id)
