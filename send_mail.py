import smtplib
import os
from dotenv import load_dotenv
load_dotenv(".env")

def send_email(recipient_email, contents):
    gmail = os.getenv("gmail")
    password_gmail = os.getenv("password_gmail")
    smtp_gmail = "smtp.gmail.com"
    sender_email = gmail

    with smtplib.SMTP(smtp_gmail, port=587) as connection:
        connection.starttls()  # secures connection to email server
        connection.login(user=gmail, password=password_gmail)
        connection.sendmail(
            from_addr=gmail,
            to_addrs=recipient_email,
            msg=f"Subject:Take an umbrella today!\n\n"
                f"{contents}")
    print("Email sent!")