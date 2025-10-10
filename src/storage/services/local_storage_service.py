import os
import tempfile
import uuid
from pathlib import Path

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile, TemporaryUploadedFile

from app import settings
from src.media.enums import MediaEnum


class LocalStorageService:
    def upload_file(self, uploaded_file: UploadedFile, file_name: str) -> dict:
        upload_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # create directory if not exists
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)

        with open(upload_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return {
            'file_name': file_name,
        }

    def temp_upload_file(self, uploaded_file: UploadedFile) -> dict:
        extension = Path(uploaded_file.name).suffix  # .jpg or .mp4
        remote_file_name = f'{uuid.uuid4()}{extension}'
        file_type = self.get_file_type(uploaded_file=uploaded_file)

        if isinstance(uploaded_file, TemporaryUploadedFile):
            local_file_path = uploaded_file.temporary_file_path()
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as local_file:
                for chunk in uploaded_file.chunks():
                    local_file.write(chunk)
                local_file_path = local_file.name

        return {
            'file_type': file_type,
            'local_file_path': local_file_path,
            'remote_file_name': remote_file_name,
        }

    def delete_file(self, file_path: str) -> None:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)

    def get_file_type(self, uploaded_file: UploadedFile) -> str:
        mime_type = uploaded_file.content_type  # e.g. "image/jpeg", "video/mp4"

        if mime_type.startswith("image/"):
            return MediaEnum.FILE_TYPE_IMAGE.value
        elif mime_type.startswith("video/"):
            return MediaEnum.FILE_TYPE_VIDEO.value
        elif mime_type.startswith("audio/"):
            return MediaEnum.FILE_TYPE_AUDIO.value
        else:
            raise Exception("Unsupported file type")
