import requests

from src.storage.init_storage import init_remote_storage
from app.log import log

class BunnyUploadFileService:
    # https://docs.bunny.net/reference/put_-storagezonename-path-filename
    def upload_file(
            self,
            local_file_path: str,
            remote_file_path: str,
            remote_file_name: str,
    ) -> dict:
        data = init_remote_storage()
        access_key = data.get('access_key')
        base_url = data.get('base_url')

        remote_full_path = f'{remote_file_path}/{remote_file_name}'
        url = f"{base_url}/{remote_full_path}"

        headers = {
            "AccessKey": access_key,
            "Content-Type": "application/octet-stream",
            "accept": "application/json"
        }

        with open(local_file_path, 'rb') as file_data:
            response = requests.put(url, headers=headers, data=file_data)

        return {
            'file_id': remote_full_path,
            'file_path': remote_full_path,
        }
