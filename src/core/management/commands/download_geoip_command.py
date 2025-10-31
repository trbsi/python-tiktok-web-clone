import gzip
import shutil
from pathlib import Path

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests import Response

from app import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.now()
        year_month = f'{now.year}-{now.month}'
        url = f"https://download.db-ip.com/free/dbip-city-lite-{year_month}.mmdb.gz"
        gzip_path = Path(f'{settings.BASE_DIR}/geoip/geoip-db.mmdb.gz')
        output_path = settings.IP_DATABASE_PATH

        print(f'Downloading from {url}...')
        response: Response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(gzip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print('Extracting...')
        with gzip.open(gzip_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        gzip_path.unlink()
        print('Done.')
