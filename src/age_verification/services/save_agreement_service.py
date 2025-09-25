from django.contrib.auth.models import Group
from django.db.models.fields.related_descriptors import ManyRelatedManager

from src.age_verification.models import PerformerAgreement, Kyc
from src.user.enum import UserEnum
from src.user.models import User


class SaveAgreementService():
    def save_agreement(self, user: User, ip: str, user_agent: str):
        PerformerAgreement.objects.create(
            user=user,
            form_type=PerformerAgreement.FORM_PERFORMER_AGREEMENT,
            form_version=1,
            ip_address=ip,
            user_agent=user_agent,
        )

        kyc = Kyc.objects.filter(user=user).exists()
        if kyc:
            performer_role = Group.objects.get_or_create(name=UserEnum.ROLE_PERFORMER.value)
            user_role = Group.objects.get_or_create(name=UserEnum.ROLE_USER.value)

            performer_role_user_set: ManyRelatedManager = performer_role.user_set
            performer_role_user_set.add(user)

            user_role_user_set: ManyRelatedManager = user_role.user_set
            user_role_user_set.remove(user)
