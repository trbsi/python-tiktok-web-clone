from pickle import format_version

from django.contrib.auth.models import Group
from django.db.models.manager import Manager

from src.age_verification.models import AgeVerification, CreatorAgreement
from src.user.enum import UserEnum
from src.user.models import User


class CreatorService:
    CURRENT_AGREEMENT_VERSION = 1

    def become_creator(self, user: User):
        age_verification = self.is_age_verification_completed(user)
        creator_agreement = self.is_creator_agreement_completed(user)

        if age_verification and creator_agreement:
            creator_role = Group.objects.get_or_create(name=UserEnum.ROLE_CREATOR.value)
            user_role = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)

            creator_role_user_set: Manager[User] = creator_role.user_set
            user_role_user_set: Manager[User] = user_role.user_set

            creator_role_user_set.add(user)
            user_role_user_set.remove(user)

    def is_age_verification_completed(self, user: User) -> bool:
        return (AgeVerification.objects
                .filter(user=user)
                .filter(status=AgeVerification.STATUS_VERIFIED)
                .exists())

    def is_creator_agreement_completed(self, user: User) -> bool:
        return (CreatorAgreement.objects
                .filter(user=user)
                .filter(form_version=self.CURRENT_AGREEMENT_VERSION)
                .exists())

    def get_age_verification(self, user: User) -> AgeVerification | None:
        return AgeVerification.objects.filter(user=user).order_by('-id').first()
