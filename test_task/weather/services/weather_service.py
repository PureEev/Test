import numpy as np
from django.core.cache import cache
from geopy.format import PRIME
from urllib3 import request
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime
from geopy.geocoders import Nominatim

def get_location_by_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="WeatherApi")
    location = geolocator.reverse((latitude, longitude), language='en', exactly_one=True)
    return location.address

def get_coordinates_by_city(city_name):
    geolocator = Nominatim(user_agent="WeatherApi")
    location = geolocator.geocode(city_name)
    return location.latitude, location.longitude


class WeatherService:

    def __new__(self):
        if not hasattr(self, "instance"):
            self.instance = super(WeatherService, self).__new__(self)
        return self.instance

    def __init__(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor= 0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"


    def get_weather_data(self, latitude, longitude):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "surface_pressure", "wind_speed_10m"],
            "minutely_15": "temperature_2m",
            "timezone": "GMT",
            "forecast_days": 1
        }


        responses = self.openmeteo.weather_api(self.url, params=params)
        response = responses[0]

        current = response.Current()

        current_temperature_2m = current.Variables(0).Value()

        current_surface_pressure = current.Variables(1).Value()

        current_wind_speed_10m = current.Variables(2).Value()

        minutely_15 = response.Minutely15()
        minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()

        minutely_15_data = {"date": pd.date_range(
            start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
            end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=minutely_15.Interval()),
            inclusive="left"
        )}

        minutely_15_data["temperature_2m"] = minutely_15_temperature_2m

        minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)

        minutely_15_dataframe["date"] = pd.to_datetime(minutely_15_dataframe["date"]).dt.tz_convert("Europe/Moscow")

        current_time_utc = pd.Timestamp(datetime.utcnow()).tz_localize("UTC")

        current_time_moscow = current_time_utc.tz_convert("Europe/Moscow")

        filtered_data = minutely_15_dataframe[minutely_15_dataframe["date"] >= current_time_moscow]

        return [{'current_temperature': current_temperature_2m,'Current_surface_pressure' :current_surface_pressure, 'Current_wind_speed_10m' :current_wind_speed_10m },filtered_data ]


    def get_weather_data_with_parametras(self, latitude, longitude, date, additional_params):

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "minutely_15": additional_params,
            "start_minutely_15": date,
            "end_minutely_15" : date
        }

        responses = self.openmeteo.weather_api(self.url, params=params)
        response = responses[0]

        Minutely15 = response.Minutely15()
        Minutely15_data = {"date": pd.date_range(
            start=pd.to_datetime(Minutely15.Time(), unit="s", utc=True),
            end=pd.to_datetime(Minutely15.TimeEnd(), unit="s", utc=True),
            inclusive="left"
        )}

        i = 0
        while i < len(additional_params):
            if 'temperature_2m' in additional_params:
                Minutely15_temperature_2m = Minutely15.Variables(i).ValuesAsNumpy()
                i+=1
                Minutely15_data["temperature_2m"] = Minutely15_temperature_2m

            if 'relative_humidity_2m' in additional_params:
                Minutely15_relative_humidity_2m = Minutely15.Variables(i).ValuesAsNumpy()
                i+=1
                Minutely15_data["relative_humidity_2m"] = Minutely15_relative_humidity_2m

            if 'precipitation_probability' in additional_params:
                Minutely15_precipitation_probability = Minutely15.Variables(i).ValuesAsNumpy()
                i+=1
                Minutely15_data["precipitation_probability"] = Minutely15_precipitation_probability

            if 'wind_speed_10m' in additional_params:
                Minutely15_wind_speed_10m = Minutely15.Variables(i).ValuesAsNumpy()
                i+=1
                Minutely15_data["wind_speed_10m"] = Minutely15_wind_speed_10m


        Minutely15_dataframe = pd.DataFrame(data=Minutely15_data)

        data = Minutely15_dataframe.to_dict(orient="list")

        return data
