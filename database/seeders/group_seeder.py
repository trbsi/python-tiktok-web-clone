from django.contrib.auth.models import Group


class GroupSeeder:
    @staticmethod
    def seed():
        Group.objects.create(name='admin')
        Group.objects.create(name='user')
        Group.objects.create(name='performer')
