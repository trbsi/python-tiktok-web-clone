import os

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile

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
