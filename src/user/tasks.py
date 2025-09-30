from celery import shared_task
from django.db.models import Q

from src.inbox.models import Message, Conversation
from src.media.enums import MediaEnum
from src.media.models import Media
from src.storage.services.remote_storage_service import RemoteStorageService


@shared_task
def delete_user_media(user_id: int):
    remote_storage_service = RemoteStorageService()
    media = Media.objects.filter(user_id=user_id).filter(status=MediaEnum.STATUS_DELETED.value)

    for item in media:
        media_item: Media = item
        remote_storage_service.delete_file(
            file_id=media_item.file_info.get('file_id'),
            file_name=media_item.file_info.get('file_name')
        )

        if media_item.file_thumbnail is not None:
            remote_storage_service.delete_file(
                file_id=media_item.file_thumbnail.get('file_id'),
                file_name=media_item.file_thumbnail.get('file_name')
            )

        if media_item.file_trailer is not None:
            remote_storage_service.delete_file(
                file_id=media_item.file_trailer.get('file_id'),
                file_name=media_item.file_trailer.get('file_name')
            )

        media_item.delete()


@shared_task
def delete_user_messages(user_id: int):
    remote_storage_service = RemoteStorageService()
    messages = Message.objects.filter(sender_id=user_id).filter(file_info__isnull=False)

    for msg in messages:
        message: Message = msg
        remote_storage_service.delete_file(
            file_id=message.file_info.get('file_id'),
            file_name=message.file_info.get('file_name')
        )

    Conversation.objects.filter(Q(sender_id=user_id) | Q(recipient_id=user_id)).delete()
