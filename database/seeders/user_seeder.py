from django.contrib.auth.models import Group

from src.user.models import User as User, UserProfile


class UserSeeder:
    @staticmethod
    def seed():
        for i in range(5):
            user = User.objects.create_user(username=f'user{i}', email=f'user{i}@mail.com', password='123456')
            user.groups.add(Group.objects.get(name='user'))
            user.save()
            UserProfile.objects.create(user=user)

            performer = User.objects.create_user(
                username=f'performer{i}', email=f'performer{i}@mail.com', password='123456')
            performer.groups.add(Group.objects.get(name='performer'))
            performer.save()
            UserProfile.objects.create(user=performer)
