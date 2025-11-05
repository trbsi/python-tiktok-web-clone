import time

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from src.core.utils import format_datetime, remote_file_path_for_conversation
from src.inbox.models import Message, Conversation
from src.inbox.tasks import task_auto_reply
from src.payment.services.spendings.spend_service import SpendService
from src.storage.crons.compress_media_task.compress_media_task import CompressMediaTask
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import task_compress_media_task
from src.user.models import User


class SendMessageService:
    def __init__(self, spend_service: SpendService | None = None):
        self.spend_service = spend_service or SpendService()

    @transaction.atomic
    def send_message(
            self,
            user: User,
            conversation_id: int,
            message_content: str | None,
            uploaded_file: UploadedFile | None = None,
    ) -> dict:
        file_info = None
        file_type = None
        conversation = Conversation.objects.get(id=conversation_id)

        if uploaded_file is not None:
            local_storage_service = LocalStorageService()
            file_upload_service = RemoteStorageService()

            time1 = time.time()
            file_data = local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
            file_type = file_data.get('file_type')
            remote_file_path = remote_file_path_for_conversation(conversation, file_data.get('remote_file_name'))
            time2 = time.time()
            print(f'time in seconds for local upload: {time2 - time1}')

            time1 = time.time()
            file_info = file_upload_service.upload_file(
                local_file_type=file_type,
                local_file_path=file_data.get('local_file_path'),
                remote_file_path=remote_file_path
            )
            time2 = time.time()
            print(f'time in seconds for remote upload: {time2 - time1}')

        message = Message.objects.create(
            sender=user,
            conversation_id=conversation_id,
            message=message_content,
            file_info=file_info,
            file_type=file_type,
        )

        if user == conversation.sender:
            conversation.read_by_recipient = False
        else:
            conversation.read_by_sender = False

        conversation.save()
        self.spend_service.spend_message(user, message)

        transaction.on_commit(
            lambda: task_compress_media_task.delay(media_id=message.id, media_type=CompressMediaTask.MEDIA_TYPE_INBOX)
        )
        transaction.on_commit(lambda: task_auto_reply.delay(message_id=message.id))

        return {
            'id': message.id,
            'created_at': format_datetime(message.created_at),
            'message': message.message,
            'attachment_url': message.get_attachment_url(),
            'sender': {
                'id': message.sender.id,
                'profile_picture': message.sender.get_profile_picture(),
                'username': message.sender.username,
            }
        }
