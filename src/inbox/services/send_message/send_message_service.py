from django.core.files.uploadedfile import UploadedFile

from app.utils import format_datetime
from src.inbox.models import Message
from src.storage.services.local_storage_service import LocalStorageService
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import compress_media_task
from src.user.models import User


class SendMessageService:
    def send_message(
            self,
            user: User,
            conversation_id: int,
            messageContent: str | None,
            uploaded_file: UploadedFile | None = None,
    ) -> dict:
        file_info = None
        file_type = None

        if uploaded_file is not None:
            local_storage_service = LocalStorageService()
            file_upload_service = RemoteStorageService()

            file_data = local_storage_service.temp_upload_file(uploaded_file=uploaded_file)
            file_type = file_data.get('file_type')

            file_info = file_upload_service.upload_file(
                local_file_path=file_data.get('local_file_path'),
                remote_file_name=file_data.get('remote_file_name')
            )

        message = Message.objects.create(
            sender=user,
            conversation_id=conversation_id,
            message=messageContent,
            file_info=file_info,
            file_type=file_type,
        )

        compress_media_task.delay(media=message)

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
