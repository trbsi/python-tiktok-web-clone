from faker import Faker

from src.payment.models import Spending, Balance
from src.user.models import User as User


class BalanceSeeder:
    @staticmethod
    def seed():
        faker = Faker()
        users = User.objects.all()
        for user in users:
            balance = Balance.objects.get(user=user)
            balance.balance = faker.random_int()
            balance.save()
            
            for user1 in users:
                Spending.objects.create(
                    by_user=user1,
                    on_user=user,
                    amount=faker.random_int(),
                    action_type=faker.word(),
                    content_id=faker.random_int(),
                )
