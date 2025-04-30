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
daily_report = []

# Prints out the weather id in the first forecast
# print(weather_data["list"][0]["weather"][0]["id"])
year, month, day = weather_data["list"][0]["dt_txt"].split(" ")[0].split("-")
reversed_date = f"Forecast for the next 12 hours ({day}-{month}-{year})"
for index in range(len(weather_data["list"])):
    hour = weather_data["list"][index]["dt_txt"].split(" ")[1][0:-3]
    feels_like = round(weather_data["list"][index]["main"]["feels_like"])
    description = weather_data["list"][index]["weather"][0]["description"]
    hourly_report = f"{hour}\t{feels_like}°C\t({description})"
    daily_report.append(hourly_report)
    # print(item["weather"][0]["id"])
    condition_codes_for_next_12_hrs.append(weather_data["list"][index]["weather"][0]["id"])
# print(condition_codes_for_next_12_hrs)
# print(reversed_date)

email_body_lines = [reversed_date] + daily_report[:4]
email_contents = "\n".join(email_body_lines)
print(email_contents)

rain = False
for code in condition_codes_for_next_12_hrs:
    if code < 700:
        rain = True
if rain:
    email_subject = f"Take an umbrella today! ☔"
    send_email(os.getenv("email_recipient"), subject=email_subject,
               contents=f"{email_contents}")
else:
    email_subject = f"No rain today! 🌂"
    send_email(os.getenv("email_recipient"), subject=email_subject,
               contents=f"{email_contents}")