import requests

from src.storage.init_storage import init_remote_storage


class BunnyDeleteFileService:
    # https://docs.bunny.net/reference/delete_-storagezonename-path-filename
    def delete_file(self, remote_file_path: str) -> None:
        data = init_remote_storage()
        access_key = data.get('storage_api_key')
        base_url = data.get('base_url')
        url = f"{base_url}/{remote_file_path}"

        headers = {"AccessKey": access_key}
        requests.delete(url, headers=headers)
