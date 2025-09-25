import random
from datetime import datetime

from django.contrib.auth.models import Group
from faker import Faker

from src.media.enums import MediaEnum
from src.media.models import Media
from src.user.enum import UserEnum


class MediaSeeder:
    @staticmethod
    def seed():
        fake = Faker()
        media = [
            'https://www.sneakalcoholbag.com/tiktok/a.mp4',
            'https://www.sneakalcoholbag.com/tiktok/b.mp4',
            'https://www.sneakalcoholbag.com/tiktok/c.mp4',
            'https://www.sneakalcoholbag.com/tiktok/d.mp4',
            'https://www.sneakalcoholbag.com/tiktok/e.mp4',
            'https://www.sneakalcoholbag.com/tiktok/f.mp4',
            'https://www.sneakalcoholbag.com/tiktok/g.mp4',
            'https://www.sneakalcoholbag.com/tiktok/h.mp4',
            'https://www.sneakalcoholbag.com/tiktok/a.jpg',
            'https://www.sneakalcoholbag.com/tiktok/b.jpg',
            'https://www.sneakalcoholbag.com/tiktok/c.jpg',
            'https://www.sneakalcoholbag.com/tiktok/d.jpg',
            'https://www.sneakalcoholbag.com/tiktok/e.jpg',
            'https://www.sneakalcoholbag.com/tiktok/f.jpg',
        ]
        thumbnails = [
            'https://www.sneakalcoholbag.com/tiktok/a.jpg',
            'https://www.sneakalcoholbag.com/tiktok/b.jpg',
            'https://www.sneakalcoholbag.com/tiktok/c.jpg',
            'https://www.sneakalcoholbag.com/tiktok/d.jpg',
            'https://www.sneakalcoholbag.com/tiktok/e.jpg',
            'https://www.sneakalcoholbag.com/tiktok/f.jpg',
        ]

        performer_groups = Group.objects.filter(name=UserEnum.ROLE_PERFORMER.value).first()
        performers = performer_groups.user_set.all()

        for performer in performers:
            for i in range(10):
                rand_media = random.choice(media)
                random_thumbnail = random.choice(thumbnails)

                Media.objects.create(
                    user=performer,
                    file_info=rand_media,
                    file_type='video' if rand_media.endswith('.mp4') else 'image',
                    file_thumbnail=random_thumbnail,
                    status=MediaEnum.STATUS_FREE.value,
                    description=fake.text(),
                    created_at=datetime.now(),
                    share_count=random.randint(1, 1000),
                    like_count=random.randint(1, 1000),
                    comment_count=random.randint(1, 1000),
                )
