import os
import re
import requests as request

from slack_bolt import App

API_URL = os.environ.get("API_URL")

if __name__ == "__main__":

    app = App(
        token=os.environ.get("SLACK_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))

    def fetch_roles() -> list[str]:
        try:
            resp = request.get(f"{API_URL}/roles", timeout=10)
            if resp.status_code != 200:
                if resp.text:
                    print(resp.status_code, resp.text)
                return []
            return resp.json()["roles"]
        except Exception as e:
            print(e)
            return []

    def handle_list_roles(say):
        if roles := fetch_roles():
            say(f"Try one of these roles: {', '.join(roles)}\n Like: `@WeatherBot 02906 pirate`")    
            return
        say("Sorry, something went wrong. Heath probably broke it.")
    
    def handle_weather(zipcode: str, role: str, say):
        try:
            resp = request.get(
                f"{API_URL}?zipcode={zipcode}&role={role}", timeout=10)
            if resp.status_code != 200:
                say("Sorry, something went wrong.")
                if resp.text:
                    say(resp.text)
                return 
            say(resp.json()["summarized_weather"])
        except Exception as e:
            say("Sorry, something went wrong. Heath probably broke it.")
            print(e)

    @app.event("app_mention")
    def handle_message(event, say):
        message = event['text'].lower()
        if re.search("list", message):
            handle_list_roles(say)
            return
        if re.search("[0-9]{5}", message):
            zipcode = re.search("[0-9]{5}", message).group(0)
            role = "pirate"
            if not (roles := fetch_roles()):
                say("Sorry, something went wrong. Heath probably broke it.")
                return
            for r in roles:
                if r in message:
                    role = r
            handle_weather(zipcode, role, say)
        else:
            say("Sorry, I didn't understand that.\nTry `@WeatherBot <zipcode> <role>`")

    app.start(port=int(os.environ.get("PORT", 3000)))
