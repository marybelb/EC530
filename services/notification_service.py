import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# Assuming you might use a service like Twilio for SMS
from twilio.rest import Client as TwilioClient

class NotificationService:
    @staticmethod
    def send_email(to_address, subject, body, from_address="noreply@healthmonitoringsystem.com"):
        """
        Sends an email to a specified address.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = from_address
            msg['To'] = to_address
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            server.send_message(msg)
            server.quit()
            print(f"Email sent successfully to {to_address}")
        except Exception as e:
            print(f"Failed to send email to {to_address}: {e}")

    @staticmethod
    def send_sms(to_number, message):
        """
        Sends an SMS message to a specified phone number.
        """
        try:
            twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
            twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
            twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

            client = TwilioClient(twilio_sid, twilio_token)
            message = client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=to_number
            )
            print(f"SMS sent successfully to {to_number}")
        except Exception as e:
            print(f"Failed to send SMS to {to_number}: {e}")
