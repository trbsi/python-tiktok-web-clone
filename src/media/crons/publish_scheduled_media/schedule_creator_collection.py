from src.media.crons.publish_scheduled_media.schedule_creator_value_object import ScheduleCreatorValueObject


class ScheduleCreatorCollection:
    def __init__(self, *schedule_creator: ScheduleCreatorValueObject):
        self.schedule_creator = schedule_creator

    def is_empty(self) -> bool:
        return len(self.schedule_creator) == 0
