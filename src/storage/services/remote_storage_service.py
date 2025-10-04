from app import settings
from src.storage.init_storage import is_backblaze, is_bunny
from src.storage.services.backblaze.backblaze_delete_file_service import BackBlazeDeleteFileService
from src.storage.services.backblaze.backblaze_download_file_service import BackBlazeDownloadFileService
from src.storage.services.backblaze.backblaze_upload_file_service import BackBlazeUploadFileService
from src.storage.services.bunny.bunny_delete_file_service import BunnyDeleteFileService
from src.storage.services.bunny.bunny_download_file_service import BunnyDownloadFileService
from src.storage.services.bunny.bunny_upload_file_service import BunnyUploadFileService


class RemoteStorageService:
    def __init__(self):
        self.backblaze_upload_file_service = BackBlazeUploadFileService()
        self.backblaze_download_file_service = BackBlazeDownloadFileService()
        self.backblaze_delete_file_service = BackBlazeDeleteFileService()
        self.bunny_upload_file_service = BunnyUploadFileService()
        self.bunny_download_file_service = BunnyDownloadFileService()
        self.bunny_delete_file_service = BunnyDeleteFileService()

    def upload_file(
            self,
            local_file_type: str,
            local_file_path: str,
            remote_file_path: str,
            bucket_name: str = '',
            additional_file_info: dict = {}
    ) -> dict:
        if is_backblaze():
            if bucket_name == '':
                bucket_name = settings.STORAGE_CONFIG.get('backblaze').get('bucket_name')

            result = self.backblaze_upload_file_service.upload_file(
                local_file_path=local_file_path,
                remote_file_name=remote_file_path,
                bucket_name=bucket_name,
                additional_file_info=additional_file_info
            )
        elif is_bunny():
            result = self.bunny_upload_file_service.upload_file(
                local_file_path=local_file_path,
                remote_file_path=local_file_type,
                remote_file_name=remote_file_path,
            )
        else:
            raise Exception('Storage provider is not defined')

        return result

    def download_file(
            self,
            file_id: str,
            file_path: str,
            local_file_path_directory: str
    ) -> str:
        if is_backblaze():
            local_file_path = self.backblaze_download_file_service.download_file(
                file_id=file_id,
                file_name=file_path,
                local_file_path_directory=local_file_path_directory
            )
        elif is_bunny():
            local_file_path = self.bunny_download_file_service.download_file(
                remote_file_path=file_path,
                local_file_path_directory=local_file_path_directory
            )

        else:
            raise Exception('Storage provider is not defined')

        return local_file_path

    def delete_file(self, file_id: str, file_path: str) -> None:
        if is_backblaze():
            self.backblaze_delete_file_service.delete_file(file_id=file_id, file_name=file_path)
        elif is_bunny():
            self.bunny_delete_file_service.delete_file(remote_file_path=file_path)

        else:
            raise Exception('Storage provider is not defined')
