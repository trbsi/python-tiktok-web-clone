from django.db.models import Q

from src.inbox.models import Message, Conversation
from src.storage.services.remote_storage_service import RemoteStorageService


class DeleteUserMessagesTask:
    def delete_user_messages(self, user_id: int):
        remote_storage_service = RemoteStorageService()
        messages = Message.objects.filter(sender_id=user_id).filter(file_info__isnull=False)

        for msg in messages:
            message: Message = msg
            remote_storage_service.delete_file(
                file_id=message.file_info.get('file_id'),
                file_path=message.file_info.get('file_path')
            )

        Conversation.objects.filter(Q(sender_id=user_id) | Q(recipient_id=user_id)).delete()
