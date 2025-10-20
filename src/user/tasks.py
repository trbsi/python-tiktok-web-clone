from celery import shared_task

from src.user.crons.delete_user_media.delete_user_media_task import DeleteUserMediaTask
from src.user.crons.delete_user_messages.delete_user_messages_task import DeleteUserMessagesTask


@shared_task
def task_delete_user_media(user_id: int):
    task = DeleteUserMediaTask()
    task.delete_user_media(user_id)


@shared_task
def task_delete_user_messages(user_id: int):
    task = DeleteUserMessagesTask()
    task.delete_user_messages(user_id)
