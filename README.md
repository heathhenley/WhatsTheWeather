# WhatsTheWeather
## Calls Weather API for a zip code and summarize with OpenAI chat model
Entirely developed for funsies, takes the weather for a zip code from [weatherapi.com](weatherapi.com)
and asks OpenAI's GPT-3.5 model to summarize the weather in a fun way. Would like to time based caching
to the weather calls (so we don't actually send the request for the weather for the same place too
often - 15 minutes? -  when it likely hasn't updated). 
