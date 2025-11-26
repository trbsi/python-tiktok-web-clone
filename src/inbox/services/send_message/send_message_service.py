import uuid

from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from src.core.utils import format_datetime
from src.inbox.models import Message, Conversation
from src.inbox.tasks import task_auto_reply
from src.payment.services.spendings.spend_service import SpendService
from src.storage.crons.compress_media_task.process_media_task import ProcessMediaTask
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import task_process_media
from src.storage.utils import remote_file_path_for_conversation
from src.user.models import User


class SendMessageService:
    def __init__(
            self,
            spend_service: SpendService | None = None,
            local_storage_service: LocalStorageService | None = None,
            remote_storage_service: RemoteStorageService | None = None,
    ):
        self.spend_service = spend_service or SpendService()
        self.local_storage_service = local_storage_service or LocalStorageService()
        self.file_upload_service = remote_storage_service or RemoteStorageService()

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
            file_data = self.local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
            file_type = file_data.get('file_type')
            local_file_path = file_data.get('local_file_path')
            extension = file_data.get('extension')
            remote_file_path = remote_file_path_for_conversation(conversation, str(uuid.uuid4()), extension)

            file_info = self.file_upload_service.upload_file(
                local_file_type=file_type,
                local_file_path=local_file_path,
                remote_file_path=remote_file_path
            )

        message = Message.objects.create(
            sender=user,
            conversation_id=conversation_id,
            message=message_content,
            file_info=file_info,
            file_type=file_type,
            is_ready=True if file_info is None else False
        )

        if user == conversation.sender:
            conversation.read_by_recipient = False
        else:
            conversation.read_by_sender = False

        conversation.deleted_by_sender = False
        conversation.deleted_by_recipient = False
        conversation.save()
        self.spend_service.spend_message(user, message)

        if uploaded_file is not None:
            transaction.on_commit(
                lambda: task_process_media.delay(
                    media_id=message.id,
                    media_type=ProcessMediaTask.MEDIA_TYPE_INBOX,
                    local_file_path=local_file_path,
                    create_thumbnail=False,
                    create_trailer=False,
                    should_compress_media=False,
                    download_from_remote=False,
                )
            )
        transaction.on_commit(lambda: task_auto_reply.delay(message_id=message.id))

        if not message.is_ready:
            tmp_message = 'Preparing the media...'
        else:
            tmp_message = message.message

        return {
            'id': message.id,
            'created_at': format_datetime(message.created_at),
            'message': tmp_message,
            'attachment_url': None,
            'sender': {
                'id': message.sender.id,
                'profile_picture': message.sender.get_profile_picture(),
                'username': message.sender.username,
            }
        }
