import threading

from django.apps import AppConfig

from .updater import TemperatureUpdater


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        temp = TemperatureUpdater()
        thread = threading.Thread(target=temp.update)
        thread.start()





