from django.db.models import QuerySet
from faker import Faker

from src.engagement.models import *


class EngagementSeeder:
    @staticmethod
    def seed():
        faker: Faker = Faker()
        media: QuerySet = Media.objects.all()

        for item in media:
            integer = faker.random_int(0, 4)
            Like.objects.create(
                user=User.objects.get(username='user' + str(integer)),
                media=item,
            )
            Share.objects.create(
                user=User.objects.get(username='user' + str(integer)),
                media=item,
            )

        for item in media:
            for i in range(20):
                integer = faker.random_int(0, 4)
                Comment.objects.create(
                    user=User.objects.get(username='user' + str(integer)),
                    media=item,
                    comment=faker.text(),
                )
