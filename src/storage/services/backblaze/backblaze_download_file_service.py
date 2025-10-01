import os.path

from b2sdk.v2 import DoNothingProgressListener

from src.storage.init_storage import init_remote_storage


class BackBlazeDownloadFileService:
    def download_file(self, file_id: str, file_name: str, local_file_path_directory: str) -> str:
        b2_api = init_remote_storage()

        os.makedirs(local_file_path_directory, exist_ok=True)

        local_file_path = f'{local_file_path_directory}/{file_id}_{file_name}'
        progress_listener = DoNothingProgressListener()
        downloaded_file = b2_api.download_file_by_id(file_id, progress_listener)
        downloaded_file.save_to(local_file_path)

        return local_file_path
