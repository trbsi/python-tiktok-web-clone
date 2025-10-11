from django.core.management import BaseCommand, call_command, CommandError

from app import settings
from database.seeders.engagement_seeder import EngagementSeeder
from database.seeders.follow_seeder import FollowSeeder
from database.seeders.group_seeder import GroupSeeder
from database.seeders.inbox_seeder import InboxSeeder
from database.seeders.media_seeder import MediaSeeder
from database.seeders.packages_seeder import PackagesSeeder
from database.seeders.payment_seeder import PaymentSeeder
from database.seeders.user_seeder import UserSeeder


class Command(BaseCommand):
    help = 'Seeds the database'

    def add_arguments(self, parser):
        parser.add_argument("env", type=str, help="local or prod")
        parser.add_argument("--truncate", action="store_true", default=False)

    def handle(self, *args, **options):
        env = options["env"]

        if env == 'prod':
            self.write('Seeding packages')
            PackagesSeeder.seed()

            self.write('Seeding groups')
            GroupSeeder.seed()

            return

        if settings.APP_ENV != 'local' and env != 'local':
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
