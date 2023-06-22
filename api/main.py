from functools import cache
import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Weather API
WEATHER_API_BASE = "https://api.weatherapi.com/v1"
WEATHER_DETAIL_URL = "https://www.weatherapi.com/weather/q"

# Prompt for GPT-3.5
GPT_PROMPTS = {
    "pirate" : "You are salty, seaworthy pirate. Given the following current weather information in JSON format, explain the current weather conditions and what one should wear. Stay in character and stay salty! Answer as a hardened sea worthy pirate captain.",
    "haiku" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a haiku about the current weather conditions and what one should wear. Answer as a haiku poet.",
    "limerick" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a limerick about the current weather conditions and what one should wear. Answer as a limerick poet.",
    "sonnet" : "You are a meteorologist poet. Given the following current weather information in JSON format, write a sonnet about the current weather conditions and what one should wear. Answer as a sonnet poet.",
    "trump" : "You are an over-the-top Donald Trump impersonator.Given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as is you were Donald Trump.",
    "shakespeare" : "You are Shakespeare, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as Shakespeare, use only a sentence or two.",
    "default" : "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as a meteorologist. Use up to a few sentences.",
    "emoji" : "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer using emojis and ONLY emojis, except to write the temperature in degrees.",
    "10words": "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and what one should wear. Answer as a meteorologist, use 10 words or fewer.",
    "3words": "You are a meteorologist, given the following current weather information in JSON format, summarize the current weather conditions and and or what one should wear using only 3 words."
}

# TODO (Heath): split this into multiple files
# Response models
class WeatherResult(BaseModel):
    summarized_weather: str
    location: str
    icon_url: str
    detail_url: str


class Roles(BaseModel):
    roles: list[str]


def get_weather_api_url(zipcode: str, mode: str = "current") -> str:
    """ Build 'weatherapi.com' url for a zipcode."""
    return f"{WEATHER_API_BASE}/{mode}.json?key={WEATHER_API_KEY}&q={zipcode}"

def get_gpt_summary(text: str, role: str) -> str:
    """Use GPT-3 to summarize the text."""
    return openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": GPT_PROMPTS[role]},
        {"role": "user", "content": "Use F or Fahrenheit for temperature, if you include it. Use mph for speeds, if needed. Use US units, not metric units. Here is the weather data:\n"},
        {"role": "user", "content": text}
      ],
      temperature=0.7,
      max_tokens=500,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )["choices"][0]["message"]["content"]

def get_current_summary_for_zip(
      zipcode: str, role: str) -> tuple[str, str, str]:
    """ Gets text summary of current weather for a zipcode.

    Extra info is returned for display (icon and location). It would be good
    to cache the weather api reponse based on time and zipcode, but for now
    we'll just call it every time and wait :)
    """
    res = requests.get(
       get_weather_api_url(zipcode, mode="search"), timeout=2).json()
    detail_url = f"{WEATHER_DETAIL_URL}/{res[0]['url']}-{res[0]['id']}"
    res = requests.get(get_weather_api_url(zipcode), timeout=2).json()
    location = f'{res["location"]["name"]}, {res["location"]["region"]}'
    icon_url = str(res["current"]["condition"]["icon"])
    forecast = str(res["current"])
    return location, icon_url, get_gpt_summary(forecast, role), detail_url

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
    location = ""
    icon_url = ""
    detail_url = ""
    try:
      location, icon_url, summary, detail_url = get_current_summary_for_zip(
         zipcode, role.lower())
      print(detail_url)
    except Exception as e:
      summary = "No summary available. 😟"
      print(e)
    return WeatherResult(
        summarized_weather=summary,
        location=location,
        icon_url=icon_url,
        detail_url=detail_url)

@app.get("/weather/roles", response_model=Roles)
async def get_roles():
    return Roles(roles=list(GPT_PROMPTS.keys()))
