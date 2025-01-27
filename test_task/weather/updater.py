import time
from datetime import datetime, timedelta, timezone


# В updater.py


class TemperatureUpdater:

    @staticmethod
    def calculate_time_for_update():
        now = datetime.now()

        minutes_passed = now.minute + now.hour * 60

        next_quarter_minutes = (minutes_passed // 15 + 1) * 15

        minutes_left = next_quarter_minutes - minutes_passed

        rounded_time = now + timedelta(minutes=minutes_left)

        rounded_time = rounded_time.replace(second=0, microsecond=0)

        naive_time = rounded_time.astimezone(timezone.utc).replace(tzinfo=None)

        return minutes_left, naive_time

    def update(self):
        from .models import City
        while True:
            minutes, future_time = self.calculate_time_for_update()
            time.sleep(minutes*60)
            City.update_temperature(future_time)


