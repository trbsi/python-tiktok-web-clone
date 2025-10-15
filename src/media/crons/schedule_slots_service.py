from datetime import time


class ScheduleSlotsService:
    SLOT_MORNING = 'morning'
    SLOT_AFTERNOON = 'afternoon'
    SLOT_EVENING = 'evening'

    @staticmethod
    def get_current_slot(local_time: time) -> tuple | None:
        for start, end, slot_name in ScheduleSlotsService._get_slots():
            if local_time >= start and local_time < end:
                return (start, end, slot_name)

        return (None, None, None)

    # Define posting slots as (start_hour, end_hour)
    @staticmethod
    def _get_slots():
        return [
            (time(8, 0), time(10, 0), ScheduleSlotsService.SLOT_MORNING),  # Morning: 8–10
            (time(14, 0), time(16, 0), ScheduleSlotsService.SLOT_AFTERNOON),  # Afternoon: 14–16
            (time(18, 0), time(20, 0), ScheduleSlotsService.SLOT_EVENING),  # Evening: 18–20
        ]
