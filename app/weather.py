from collections import namedtuple
import httpx
import os

City = namedtuple("City", ["lat", "lon"])
Weather = namedtuple(
        "Weather",
        [
            "temp",
            "feels_like",
            "description",
            ]
        )
weather_api = os.getenv("OPENWEATHER_TOKEN")


async def get_city(city: str) -> City:
    params = {
            "q": city,
            "appid": weather_api
            }

    async with httpx.AsyncClient() as client:
        response = await client.get(
                url="http://api.openweathermap.org/geo/1.0/direct",
                params=params,
                )

    return City(response.json()[0]["lat"], response.json()[0]["lon"])


async def get_weather(city: City) -> Weather:
    params = {
            "lat": city.lat,
            "lon": city.lon,
            "lang": "en",
            "units": "metric",
            "appid": weather_api,
            }

    async with httpx.AsyncClient() as client:
        response = await client.get(
                url="https://api.openweathermap.org/data/2.5/weather",
                params=params,
                )

    return Weather(
            response.json()["main"]["temp"],
            response.json()["main"]["feels_like"],
            response.json()["weather"][0]["description"],
            )
