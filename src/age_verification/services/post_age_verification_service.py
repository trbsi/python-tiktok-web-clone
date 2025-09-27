from django.contrib.auth.models import Group
from django.db.models.manager import Manager

from src.age_verification.models import Kyc, CreatorAgreement
from src.user.enum import UserEnum
from src.user.models import User


class PostAgeVerificationService:
    def post_age_verification(self, user: User):
        kyc = Kyc.objects.filter(user=user).exists()
        creator_agreement = CreatorAgreement.objects.filter(user=user).exists()

        if kyc and creator_agreement:
            creator_role = Group.objects.get_or_create(name=UserEnum.ROLE_CREATOR.value)
            user_role = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)

            creator_role_user_set: Manager[User] = creator_role.user_set
            user_role_user_set: Manager[User] = user_role.user_set

            creator_role_user_set.add(user)
            user_role_user_set.remove(user)
