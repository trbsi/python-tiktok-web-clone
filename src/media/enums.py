from enum import Enum
from typing import Tuple


class MediaEnum(Enum):
    STATUS_FREE = 'free'
    STATUS_PAID = 'paid'
    STATUS_PENDING = 'pending'
    STATUS_PRIVATE = 'private'
    STATUS_DELETED = 'deleted'

    FILE_TYPE_AUDIO = 'audio'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_IMAGE = 'image'

    UNLOCK_PERMANENT = 'permanent'
    UNLOCK_SESSION = 'session'
    UNLOCK_24H = '24h'

    @staticmethod
    def statuses() -> Tuple:
        return (
            (MediaEnum.STATUS_FREE.value, 'Free'),
            (MediaEnum.STATUS_PAID.value, 'Paid'),
            (MediaEnum.STATUS_PRIVATE.value, 'Private'),
            (MediaEnum.STATUS_PENDING.value, 'Pending'),
            (MediaEnum.STATUS_DELETED.value, 'Deleted'),
        )

    @staticmethod
    def creator_statuses() -> Tuple:
        return (
            (MediaEnum.STATUS_PAID.value, 'Paid'),
            (MediaEnum.STATUS_FREE.value, 'Free'),
            (MediaEnum.STATUS_PRIVATE.value, 'Private'),
        )

    @staticmethod
    def file_types() -> Tuple:
        return (
            (MediaEnum.FILE_TYPE_AUDIO.value, 'Audio'),
            (MediaEnum.FILE_TYPE_VIDEO.value, 'Video'),
            (MediaEnum.FILE_TYPE_IMAGE.value, 'Image'),
        )

    @staticmethod
    def unlock_types() -> Tuple:
        return (
            (MediaEnum.UNLOCK_PERMANENT.value, 'Permanent'),
            (MediaEnum.UNLOCK_SESSION.value, 'Session'),
            (MediaEnum.UNLOCK_24H.value, '24H'),
        )
