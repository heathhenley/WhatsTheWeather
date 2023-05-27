# WhatsTheWeather
## Calls NOAA Weather API for a zip code and summarize with OpenAI chat model
Entirely developed for funsies - looks up the zipcode (there are still some problems with this)
on Google Maps API to get the lat/lon. Then uses that lat/lon to get the weather from NOAA's API.
Finally, call OpenAI GPT-3 model to summarize the weather in a fun way. It's a little slow due to
all the required API calls, there's a lot of places where caching could help (eg zip codes to lat/lon). 
