from src.payment.models import Package


class PackagesSeeder:
    @staticmethod
    def seed():
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
