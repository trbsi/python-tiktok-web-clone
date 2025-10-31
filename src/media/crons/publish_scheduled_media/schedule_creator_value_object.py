class ScheduleCreatorValueObject:
    def __init__(
            self,
            timezone: str,
            minutes_left: int,
            current_slot_name: str,
            number_of_creators: int,
    ):
        """
        :param timezone: name of a timezone
        :param minutes_left: number of minutes left until the end of the slot.
        :param current_slot_name: name of the slot: morning, evening...
        :param number_of_creators: number of creators that match time time slot and has scheduled posts.
        """
        self.timezone = timezone
        self.minutes_left = minutes_left
        self.current_slot_name = current_slot_name
        self.number_of_creators = number_of_creators

    def process_creators_per_minute_count(self):
        return self.number_of_creators / self.minutes_left
