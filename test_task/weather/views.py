from django.shortcuts import render
from django.http import JsonResponse

from .models import FutureTemperature, City
from .services import WeatherService
from .services.weather_service import get_location_by_coordinates, get_coordinates_by_city

instance = WeatherService()


def get_weather_by_coordinate(request):
    weather_data = None
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        if latitude is None or longitude is None:
            return render(request, 'weather/weather.html', {'weather_data':weather_data})
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return JsonResponse({"error": "Longitude and latitude must be valid numbers"}, status = 400)

        if latitude > 90 or latitude < -90:
            return JsonResponse({"error": "Wrong format for latitude"}, status = 400)
        if longitude > 180 or longitude < -180:
            return JsonResponse({"error": "Wrong format for longitude"}, status = 400)

        weather_data = instance.get_weather_data(latitude, longitude)

    return render(request, 'weather/weather.html', {'weather_data':weather_data[0]})


def add_city(request):
    city_added = None
    if request.method == 'GET':

        city = request.GET.get('city')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        if latitude is None or longitude is None:
            return render(request, 'weather/additing_city.html', {'city_added':city_added})
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return JsonResponse({"error": "Longitude and latitude must be valid numbers"}, status = 400)

        if latitude > 90 or latitude < -90:
            return JsonResponse({"error": "Wrong format for latitude"}, status = 400)
        if longitude > 180 or longitude < -180:
            return JsonResponse({"error": "Wrong format for longitude"}, status = 400)

        if latitude is None or longitude is None:
            return render(request, 'weather/additing_city.html', {'city_added':city_added})

        weather_data = instance.get_weather_data(latitude, longitude)

        FutureTemperature.add_data(city, weather_data[0]['current_temperature'], weather_data[1])

        city_added = city

    return render(request, 'weather/additing_city.html', {'city_added': city_added})


def get_cities_list(request):
    response_data = {}
    if request.method == 'GET':
        response_data['Cities'] = City.objects.values('city_name')

    return render(request, 'weather/cities.html',response_data )

def get_weather_by_city_and_time(request):
    weather_data = None
    if request.method == 'GET':
        city = request.GET.get('city')
        date = request.GET.get('time')

        if city is None or date is None:
            return render(request,'weather/weather_with_parametras.html', {'weather_data':weather_data})

        selected_parameters = {"temperature_2m" : False, "relative_humidity_2m": False, "precipitation_probability": False, "wind_speed_10m": False}

        if request.GET.get('temperature'):
            selected_parameters["temperature_2m"] = True
        if request.GET.get('humidity'):
            selected_parameters["relative_humidity_2m"] = True
        if request.GET.get('wind_speed'):
            selected_parameters["wind_speed_10m"] = True
        if request.GET.get('precipitation'):
            selected_parameters["precipitation_probability"] = True

        selected_parameters = [param for param in selected_parameters.keys() if selected_parameters[param]==True]
        latitude, longitude = get_coordinates_by_city(city)
        weather_data = instance.get_weather_data_with_parametras(latitude, longitude,date, selected_parameters)


    return render(request, 'weather/weather_with_parametras.html', {'weather_data':weather_data})

