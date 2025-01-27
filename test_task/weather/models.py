from django.db import models
from django.utils import timezone


# Create your models here.

class City(models.Model):
    city_name = models.CharField(max_length = 40, unique= True)
    current_temperature = models.DecimalField(max_digits=4, decimal_places=2)

    @staticmethod
    def update_temperature(time):

        if timezone.is_naive(time):
            time = timezone.make_aware(time, timezone.get_default_timezone())

        temperatures = FutureTemperature.objects.filter(time=time)
        cities = City.objects.all()
        for city in cities:
            temp = temperatures.filter(city = city).first()
            if not temp:
                city.delete()
            else:
                city.current_temperature = temp.future_temperature
                city.save()
                temp.delete()


class FutureTemperature(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name= "temperatures")
    future_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    time = models.DateTimeField()

    @staticmethod
    def add_data(city_name, current_temperature, future_temperature_data):

        city, created = City.objects.get_or_create(city_name=city_name,
                                                   defaults={'current_temperature': current_temperature})
        if not created:
            city.current_temperature = current_temperature
            city.save()

        for _, temp_data in future_temperature_data.iterrows():
            time = temp_data['date']
            future_temp = temp_data['temperature_2m']
            FutureTemperature.objects.create(
                city=city,
                future_temperature=future_temp,
                time=time
            )