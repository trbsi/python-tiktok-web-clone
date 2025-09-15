import random
from datetime import datetime

from faker import Faker

from src.media.enums import MediaEnum
from src.media.models import Media
from src.user.models import User as User


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
        for i in range(100):
            performer_name = 'performer' + str(fake.random_int(min=0, max=4))
            rand_media = random.choice(media)

            Media.objects.create(
                user=User.objects.get(username=performer_name),
                file=rand_media,
                file_type='video' if rand_media.endswith('.mp4') else 'image',
                file_thumbnail=rand_media,
                status=MediaEnum.STATUS_FREE.value,
                description=fake.text(),
                created_at=datetime.now(),
                share_count=random.randint(1, 1000),
                like_count=random.randint(1, 1000),
                comment_count=random.randint(1, 1000),
            )
