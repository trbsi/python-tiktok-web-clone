from src.media.crons.publish_scheduled_media.scheduled_media_value_object import ScheduledMediaValueObject


class ScheduledMediaCollection:
    def __init__(self, *scheduled_media: ScheduledMediaValueObject):
        self.scheduled_media = scheduled_media

    def is_empty(self) -> bool:
        return len(self.scheduled_media) == 0
