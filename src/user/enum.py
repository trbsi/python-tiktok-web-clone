from enum import Enum


class UserEnum(Enum):
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_PERFORMER = 'performer'

    @staticmethod
    def roles():
        return (
            (UserEnum.ROLE_USER, 'User'),
            (UserEnum.ROLE_PERFORMER, 'Performer'),
        )
