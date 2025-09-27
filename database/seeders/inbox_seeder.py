import random
from pathlib import Path

from django.db.models import QuerySet
from faker import Faker

from src.inbox.models import Conversation, Message
from src.media.enums import MediaEnum
from src.user.models import User
from .media_data import media_list


class InboxSeeder():
    @staticmethod
    def seed():
        faker = Faker()
        performers: QuerySet = User.objects.filter(groups__name='performer')
        users: QuerySet = User.objects.filter(groups__name='user')

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
                        file_info: dict = random.choice(media_list)
                        extension = Path(file_info.get('file_name')).suffix
                        file_type = MediaEnum.FILE_TYPE_IMAGE.value if extension == '.jpg' else MediaEnum.FILE_TYPE_VIDEO.value

                    Message.objects.create(
                        conversation=conversion,
                        sender=performer if i % 2 == 0 else user,
                        message=f'{i}. {faker.text()}',
                        file_info=file_info,
                        file_type=file_type,
                    )
