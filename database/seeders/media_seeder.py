import random
from datetime import datetime

from faker import Faker

from src.media.models import Media
from src.user.models import User as User


class MediaSeeder:
    @staticmethod
    def seed():
        fake = Faker()
        videos = [
            'https://assets.mixkit.co/videos/40063/40063-720.mp4',
            'https://assets.mixkit.co/videos/51202/51202-720.mp4',
            'https://assets.mixkit.co/videos/41236/41236-720.mp4',
            'https://assets.mixkit.co/videos/1258/1258-720.mp4',
            'https://assets.mixkit.co/videos/40464/40464-720.mp4',
        ]
        for i in range(100):
            performer_name = 'performer' + str(fake.random_int(min=0, max=4))
            Media.objects.create(
                user=User.objects.get(username=performer_name),
                file=random.choice(videos),
                file_type='video',
                status='public',
                description=fake.text(),
                created_at=datetime.now(),
                share_count=random.randint(1, 1000),
            )
