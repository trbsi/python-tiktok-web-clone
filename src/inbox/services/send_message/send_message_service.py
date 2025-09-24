import tempfile
import uuid
from pathlib import Path

from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

from app import settings
from src.inbox.models import Message
from src.storage.services.remote_storage_service import RemoteStorageService
from src.storage.tasks import compress_media_task
from src.user.models import User


class SendMessageService:
    def send_message(
            self,
            user: User,
            conversation_id: int,
            messageContent: str | None,
            file: UploadedFile | None = None,
    ) -> dict:
        file_info = None
        if file is not None:
            if isinstance(file, TemporaryUploadedFile):
                local_file_path = file.temporary_file_path()
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as local_file:
                    for chunk in file.chunks():
                        local_file.write(chunk)
                    local_file_path = local_file.name

            extension = Path(file.name).suffix
            remote_file_name = f'{uuid.uuid4()}.{extension}'

            file_upload_service = RemoteStorageService()
            file_info = file_upload_service.upload_file(
                local_file_path=local_file_path,
                remote_file_name=remote_file_name
            )

        message = Message.objects.create(
            sender=user,
            conversation_id=conversation_id,
            message=messageContent,
            file_info=file_info,
        )

        compress_media_task.delay(media_type='inbox', media_id=message.id)

        return {
            'id': message.id,
            'created_at': message.created_at.strftime(settings.DATE_TIME_FORMAT),
            'message': message.message,
            'attachment_url': message.get_attachment_url(),
            'sender': {
                'id': message.sender.id,
                'profile_picture': message.sender.get_profile_picture(),
                'username': message.sender.username,
            }
        }
