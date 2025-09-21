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

        for performer in performers:
            for user in users:
                conversion = Conversation.objects.create(
                    recipient=performer,
                    sender=user,
                    last_message=faker.text(),
                )
                for i in range(100):
                    Message.objects.create(
                        conversation=conversion,
                        sender=performer if i % 2 == 0 else user,
                        content=f'{i}. {faker.text()}',
                    )
