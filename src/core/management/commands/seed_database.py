from pathlib import Path

from django.core.management import BaseCommand, call_command, CommandError

from app import settings
from database.seeders import *


class Command(BaseCommand):
    help = 'Seeds the database'

    def add_arguments(self, parser):
        parser.add_argument("--truncate", action="store_true", default=False)
        parser.add_argument("--drop", action="store_true", default=False)

    def handle(self, *args, **options):
        if settings.APP_ENV != 'local':
            raise CommandError('You are not in local env')

        should_truncate = options["truncate"]
        drop = options["drop"]

        if drop:
            database = Path(settings.DATABASES['default']['NAME'])
            if database.exists():
                database.unlink()
            database.touch()
            database.chmod(0o666)
            self.stdout.write(self.style.SUCCESS('Database dropped. Run without drop to seed'))
            return

        if should_truncate:
            call_command("flush", interactive=False)

        call_command("makemigrations", interactive=False)
        call_command("migrate")

        GroupSeeder().seed()
        UserSeeder().seed()
        MediaSeeder().seed()
        EngagementSeeder().seed()

        self.stdout.write(self.style.SUCCESS('Done'))
