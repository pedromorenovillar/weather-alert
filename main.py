import requests
import os
from dotenv import load_dotenv
load_dotenv(".env")

from send_mail import send_email


OWM_endpoint = os.getenv("OWM_endpoint")
api_key = os.getenv("api_key")
lat = os.getenv("lat")
lon = os.getenv("lon")

# lat and long for a place where is currently raining as in https://www.ventusky.com/
# lat = 36.116
# lon = -97.059

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric",
    "cnt": 4,
}

current = "weather"
forecast = "forecast"

response = requests.get(OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# Creates a list of the weather condition codes
condition_codes_for_next_12_hrs = []

# Prints out the weather id in the first forecast
# print(weather_data["list"][0]["weather"][0]["id"])
for item in weather_data["list"]:
    # print(item["weather"][0]["id"])
    condition_codes_for_next_12_hrs.append(item["weather"][0]["id"])
print(condition_codes_for_next_12_hrs)
rain = False
for code in condition_codes_for_next_12_hrs:
    if code < 700:
        rain = True
if rain:
    send_email(os.getenv("email_recipient"), contents="It's going to rain today. Bring an umbrella with you.")
else:
    print('No rain')