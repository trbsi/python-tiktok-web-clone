import random

from faker import Faker

from src.engagement.models import Comment
from src.inbox.models import Message
from src.media.models import Media
from src.payment.models import Spending, Balance, Package
from src.user.models import User as User


class PaymentSeeder:
    @staticmethod
    def seed():
        faker = Faker()
        users = User.objects.all()

        objects = [Comment.objects.first(), Media.objects.first(), Message.objects.first()]

        for user in users:
            balance = Balance.objects.get(user=user)
            balance.balance = 0
            balance.save()

            spending = 0
            for user1 in users:
                amount = faker.random_int()
                spending += amount
                Spending.objects.create(
                    by_user=user1,
                    on_user=user,
                    amount=amount,
                    content_object=random.choice(objects),
                )

            balance.balance = spending
            balance.save()

        packages = [
            {'price': '0.99', 'amount': 100, 'bonus': None},
            {'price': '4.99', 'amount': 499, 'bonus': None},
            {'price': '9.99', 'amount': 999, 'bonus': None},
            {'price': '19.99', 'amount': 1999, 'bonus': None},
            {'price': '49.99', 'amount': 4999, 'bonus': None},
            {'price': '99.99', 'amount': 9999, 'bonus': None},
        ]

        for package in packages:
            Package.objects.create(
                price=package['price'],
                amount=package['amount'],
                bonus=package['bonus'],
            )
