from enum import Enum
from typing import Tuple


class InboxEnum(Enum):
    STATUS_ACTIVE = 'active'
    STATUS_DELETED = 'deleted'

    @staticmethod
    def statuses() -> Tuple:
        return (
            (InboxEnum.STATUS_ACTIVE.value, 'Active'),
            (InboxEnum.STATUS_DELETED.value, 'Deleted'),
        )
