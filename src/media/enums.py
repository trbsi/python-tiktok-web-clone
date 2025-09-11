from enum import Enum
from typing import Tuple


class MediaEnum(Enum):
    STATUS_PUBLIC = 'public'
    STATUS_PENDING = 'pending'
    STATUS_LOCKED = 'locked'
    STATUS_PRIVATE = 'private'
    STATUS_DELETED = 'deleted'

    FILE_TYPE_AUDIO = 'audio'
    FILE_TYPE_VIDEO = 'video'
    FILE_TYPE_IMAGE = 'image'

    @staticmethod
    def statuses() -> Tuple:
        return (
            (MediaEnum.STATUS_PUBLIC.value, 'Public'),
            (MediaEnum.STATUS_PRIVATE.value, 'Private'),
            (MediaEnum.STATUS_PENDING.value, 'Pending'),
            (MediaEnum.STATUS_LOCKED.value, 'Locked'),
            (MediaEnum.STATUS_DELETED.value, 'Deleted'),
        )

    @staticmethod
    def file_types() -> Tuple:
        return (
            (MediaEnum.FILE_TYPE_AUDIO.value, 'Audio'),
            (MediaEnum.FILE_TYPE_VIDEO.value, 'Video'),
            (MediaEnum.FILE_TYPE_IMAGE.value, 'Image'),
        )
