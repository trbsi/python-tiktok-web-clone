import requests

from src.storage.init_storage import init_remote_storage


class BunnyDownloadFileService:
    # https://docs.bunny.net/reference/get_-storagezonename-path-filename
    def download_file(self, remote_file_path: str, local_file_path_directory: str) -> str:
        data = init_remote_storage()
        access_key = data.get('storage_api_key')
        storage_zone_name = data.get('storage_zone_name')
        base_url = data.get('base_url')

        local_file_path = f'{local_file_path_directory}/{remote_file_path}'

        remote_full_path = f'{storage_zone_name}/{remote_file_path}'
        url = f"https://{base_url}/{remote_full_path}"

        headers = {
            "accept": "*/*",
            "AccessKey": access_key
        }

        # Stream download to handle large files
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(local_file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return local_file_path
