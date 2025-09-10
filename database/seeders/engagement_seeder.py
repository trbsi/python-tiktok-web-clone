from django.db.models import QuerySet
from faker import Faker

from src.engagement.models import *


class EngagementSeeder:
    @staticmethod
    def seed():
        faker: Faker = Faker()
        media: QuerySet[Media] = Media.objects.all()

        for media_item in media:
            integer = faker.random_int(0, 4)
            Like.objects.create(
                user=User.objects.get(username='user' + str(integer)),
                media=media_item,
            )
            Share.objects.create(
                user=User.objects.get(username='user' + str(integer)),
                media=media_item,
            )

            media_item.like_count = media_item.like_count + 1
            media_item.save()

        for media_item in media:
            for i in range(20):
                integer = faker.random_int(0, 4)
                Comment.objects.create(
                    user=User.objects.get(username='user' + str(integer)),
                    media=media_item,
                    comment=faker.text(),
                )

                media_item.comment_count = media_item.comment_count + 1
                media_item.save()
