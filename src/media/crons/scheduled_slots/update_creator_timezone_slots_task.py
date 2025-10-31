import zoneinfo
from datetime import datetime

from src.media.crons.schedule_slots_service import ScheduleSlotsService
from src.media.models import MediaScheduler


class UpdateCreatorTimezoneSlotsTask:
    def update_timezone_slots(self):
        """
        Runs through all timezones and updates the scheduled slots based on timezone local time and available slots
        If there is no matched time slot based on time null will be saved
        E.g. If there is 9am in LA timezone, slot will be updated to "morning"
        """
        timezones = MediaScheduler.objects.values_list('timezone', flat=True).distinct()

        for timezone in timezones:
            tz = zoneinfo.ZoneInfo(timezone)
            local_time = datetime.now(tz).time()

            start, end, slot_name = ScheduleSlotsService.get_current_slot(local_time)
            MediaScheduler.objects.filter(timezone=timezone).update(current_slot=slot_name)
