import smtplib
import os
from dotenv import load_dotenv
load_dotenv(".env")

from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def send_email(recipient_email, subject, contents):
    gmail = os.getenv("gmail")
    password_gmail = os.getenv("password_gmail")
    smtp_gmail = "smtp.gmail.com"
    sender_email = gmail

    msg = MIMEText(contents, _charset="utf-8")
    msg["From"] = formataddr(("Weather Alert", gmail))
    msg["To"] = recipient_email
    msg["Subject"] = Header(subject, "utf-8")

    with smtplib.SMTP(smtp_gmail, port=587) as connection:
        connection.starttls()  # secures connection to email server
        connection.login(user=gmail, password=password_gmail)
        connection.sendmail(
            from_addr=gmail,
            to_addrs=recipient_email,
            msg=msg.as_string()
        )