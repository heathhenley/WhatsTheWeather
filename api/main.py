from functools import cache
import os
import requests

from fastapi import FastAPI
from pydantic import BaseModel

import openai

googgle_api_key = os.getenv("GOOGLE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# NOAA Weather API
NOAA_API_BASE = "https://api.weather.gov"
NOAA_API_APP_NAME = "whats-the-weather"

# Google Maps API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MAPS_API_BASE = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"

# Prompt for GPT-3
GPT_PROMPTS = {
    "pirate" : "You are salty, seaworthy pirate. Given the following current weather information in JSON format, explain the current weather conditions and what one should wear. Stay in character and stay salty! Answer as a hardened sea worthy pirate captain. Use only a sentence or two.",
    "haiku" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a haiku about the current weather conditions and what one should wear. Answer as a haiku poet.",
    "limerick" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a limerick about the current weather conditions and what one should wear. Answer as a limerick poet."
}


def get_noaa_forecast_url(lat: float, lon: float) ->  tuple[int, int]:
    """Get the NOAA gridpoint for a latitude and longitude.
    """
    return requests.get(
        f"{NOAA_API_BASE}/points/{lat},{lon}",
        timeout=2).json()["properties"]["forecast"]

@cache
def zip_to_lat_lon(zipcode: str) -> tuple[float, float]:
    """Convert a zipcode to a latitude and longitude."""
    resp = requests.get(GOOGLE_MAPS_API_BASE.format(zipcode, GOOGLE_API_KEY), timeout=2).json()['results'][0]
    geom = resp['geometry']['bounds']['northeast']
    return (geom['lat'], geom['lng'])

@cache
def zip_to_forecast_url(zipcode: str) -> str:
    """ Use NOAA API to query the forecase URL for this zipcode."""
    return get_noaa_forecast_url(*zip_to_lat_lon(zipcode))

def get_gpt_summary(text: str, role: str) -> str:
    """Use GPT-3 to summarize the text."""
    return openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": GPT_PROMPTS[role]},
        {"role": "user", "content": text}
      ],
      temperature=0.7,
      max_tokens=1000,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )["choices"][0]["message"]["content"]

def get_current_summary_for_zip(zipcode: str, role: str) -> str:
    forecast_url = zip_to_forecast_url(zipcode)
    forecast = requests.get(forecast_url, timeout=2).json()
    weather_info = str(forecast["properties"]["periods"][0])
    return get_gpt_summary(weather_info, role)


class WeatherResult(BaseModel):
    summarized_weather: str


@app.get("/weather", response_model=WeatherResult)
def weather(zipcode: str = "02906", role: str = "pirate"):
    """Get the weather for a zipcode."""
    try:
      summary = get_current_summary_for_zip(zipcode, role)
    except Exception as e:
      summary = "No summary available."
      print(e)
    return WeatherResult(
        summarized_weather=summary)