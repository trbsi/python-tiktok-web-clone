from django.db.models import QuerySet
from faker import Faker

from src.inbox.models import Conversation, Message
from src.user.models import User


class InboxSeeder():
    @staticmethod
    def seed():
        faker = Faker()
        performers: QuerySet = User.objects.filter(groups__name='performer')
        users: QuerySet = User.objects.filter(groups__name='user')
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

        for performer in performers:
            for user in users:
                conversion = Conversation.objects.create(
                    recipient=performer,
                    sender=user,
                    last_message=faker.text(),
                )
                for i in range(100):
                    file_info = None
                    file_type = None
                    if i % 5 == 0:
                        pass
                        # TODO finish file_info
                        # file_info = {random.choice(media)}
                        # extension = Path(file_info.get('file_name')).suffix
                        # file_type = MediaEnum.FILE_TYPE_IMAGE.value if extension == 'jpg' else MediaEnum.FILE_TYPE_VIDEO.value

                    Message.objects.create(
                        conversation=conversion,
                        sender=performer if i % 2 == 0 else user,
                        message=f'{i}. {faker.text()}',
                        file_info=file_info,
                        file_type=file_type,
                    )
