from django.core.management import BaseCommand, call_command, CommandError

from app import settings
from database.seeders import *
from database.seeders.follow_seeder import FollowSeeder
from database.seeders.inbox_seeder import InboxSeeder
from database.seeders.payment_seeder import PaymentSeeder


class Command(BaseCommand):
    help = 'Seeds the database'

    def add_arguments(self, parser):
        parser.add_argument("--truncate", action="store_true", default=False)

    def handle(self, *args, **options):
        if settings.APP_ENV != 'local':
            raise CommandError('You are not in local env')

        should_truncate = options["truncate"]

        if should_truncate:
            call_command("flush", interactive=False)

        call_command("makemigrations", interactive=False)
        call_command("migrate")

        self.write('Seeding groups')
        GroupSeeder.seed()

        self.write('Seeding users')
        UserSeeder.seed()

        self.write('Seeding media')
        MediaSeeder.seed()

        self.write('Seeding engagement')
        EngagementSeeder.seed()

        self.write('Seeding inbox')
        InboxSeeder.seed()

        self.write('Seeding followers')
        FollowSeeder.seed()

        self.write('Seeding balance')
        PaymentSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Done'))

    def write(self, string: str) -> None:
        self.stdout.write(self.style.SUCCESS(string))
