import requests
import os
from dotenv import load_dotenv
load_dotenv(".env")
from send_mail import send_email

# Loads environment variables
OWM_endpoint = os.getenv("OWM_endpoint")
api_key = os.getenv("api_key")
lat = os.getenv("lat")
lon = os.getenv("lon")
recipient_email = os.getenv("email_recipient")

# Sets weather params for OWM API
weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "metric",
    "cnt": 6,
}

# Calls API and retrieves response
response = requests.get(OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# Creates a list of the weather condition codes and a daily report
condition_codes_for_next_12_hrs = []
daily_report = []

# Creates email body header
year, month, day = weather_data["list"][0]["dt_txt"].split(" ")[0].split("-")
reversed_date = f"Forecast for today, {day}-{month}-{year}\n" + ("-" * 35)

# Extracts data for email report
for index in range(len(weather_data["list"])):
    hour = weather_data["list"][index]["dt_txt"].split(" ")[1][0:-3]
    feels_like = round(weather_data["list"][index]["main"]["feels_like"])
    description = weather_data["list"][index]["weather"][0]["description"].capitalize()
    hourly_report = f"{hour}\t{feels_like}°C\t{description}"
    daily_report.append(hourly_report)
    condition_codes_for_next_12_hrs.append(weather_data["list"][index]["weather"][0]["id"])

# Creates email contents
email_body_lines = [reversed_date] + daily_report[:6]
email_contents = "\n".join(email_body_lines)
print(email_contents)

# Sends email with different subject lines if it is going to rain
rain = False
for code in condition_codes_for_next_12_hrs:
    if code < 700:
        rain = True
if rain:
    email_subject = f"Take an umbrella today! ☔"
    send_email(recipient_email=recipient_email, subject=email_subject,
               contents=f"{email_contents}")
else:
    email_subject = f"No rain today! 🌂"
    send_email(recipient_email=recipient_email, subject=email_subject,
               contents=f"{email_contents}")