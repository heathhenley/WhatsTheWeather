from functools import cache
import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import openai

googgle_api_key = os.getenv("GOOGLE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    "limerick" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a limerick about the current weather conditions and what one should wear. Answer as a limerick poet.",
    "c3po" : "You C3PO, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as C3PO, use only a sentence or two.",
    "r2d2" : "You are R2D2, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as R2D2, the robot, add some beeps and boops, use only a sentence or two. Make sure to beep and boop.",
    "yoda" : "You are Yoda, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as Yoda, use only a sentence or two.",
    "shakespeare" : "You are Shakespeare, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as Shakespeare, use only a sentence or two.",
    "default" : "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as a meteorologist, use only a sentence or two.",
    "emoji" : "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer using emojis and ONLY emojis, except to write the temperature in degrees.",
    "10words": "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as a meteorologist, use 10 words or fewer.",
    "3words": "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and and or what one should wear using only 3 words."
}

# TODO (Heath): split this into multiple files
# Response models
class WeatherResult(BaseModel):
    summarized_weather: str

class Roles(BaseModel):
    roles: list[str]

def get_noaa_forecast_url(lat: float, lon: float) ->  tuple[int, int]:
    """Get the NOAA gridpoint for a latitude and longitude.
    """
    res = requests.get(
        f"{NOAA_API_BASE}/points/{lat:.4f},{lon:.4f}",
        timeout=5).json()
    return res["properties"]["forecast"]

@cache
def zip_to_lat_lon(zipcode: str) -> tuple[float, float]:
    """Convert a zipcode to a latitude and longitude."""
    try:
        resp = requests.get(
           GOOGLE_MAPS_API_BASE.format(zipcode, GOOGLE_API_KEY),
           timeout=5).json()['results'][0]
    except Exception as e:
        print(f"call to google api failed {e}")
        print(GOOGLE_MAPS_API_BASE.format(zipcode, GOOGLE_API_KEY))
        raise e
    geom = resp['geometry']['location']
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
      max_tokens=500,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )["choices"][0]["message"]["content"]

def get_current_summary_for_zip(zipcode: str, role: str) -> str:
    forecast_url = zip_to_forecast_url(zipcode)
    forecast = requests.get(forecast_url, timeout=2).json()
    weather_info = str(forecast["properties"]["periods"][0])
    return get_gpt_summary(weather_info, role)

@app.get("/weather", response_model=WeatherResult)
async def weather(zipcode: str = "02906", role: str = "default"):
    """Get the weather for a zipcode."""
    role = role.lower()
    if role not in GPT_PROMPTS:
      raise HTTPException(
          status_code=404,
          detail=f"Role not found. Try one of these: {', '.join(GPT_PROMPTS.keys())}")
    if len(zipcode) != 5:
      raise HTTPException(
          status_code=404,
          detail="Zipcode must be 5 digits.")
    try:
      summary = get_current_summary_for_zip(zipcode, role.lower())
    except Exception as e:
      summary = "No summary available. 😟"
      print(e)
    return WeatherResult(
        summarized_weather=summary)

@app.get("/weather/roles", response_model=Roles)
async def get_roles():
    return Roles(roles=list(GPT_PROMPTS.keys()))
