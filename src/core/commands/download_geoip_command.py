import requests
from celery.utils.time import timezone
from django.core.management.base import BaseCommand
from requests import Response

from app import settings


class DownloadGeoIpCommand(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.now()
        year_month = f'{now.year}-{now.month}'
        url = f"https://download.db-ip.com/free/dbip-city-lite-{year_month}.mmdb.gz"
        output_path = settings.IP_DATABASE_PATH

        print('Downloading...')
        response: Response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
