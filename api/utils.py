import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid

def send_email(to_address, subject, body, from_address="noreply@healthmonitoring.com", smtp_server="smtp.example.com", smtp_port=587, smtp_user="user", smtp_password="password"):
    """
    Sends an email using SMTP.
    """
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def generate_uuid():
    """
    Generates a unique identifier.
    """
    return uuid.uuid4().hex

def format_datetime(dt, format="%Y-%m-%d %H:%M:%S"):
    """
    Formats a datetime object to a string.
    """
    return dt.strftime(format)

def parse_datetime(dt_str, format="%Y-%m-%d %H:%M:%S"):
    """
    Parses a datetime string to a datetime object.
    """
    return datetime.strptime(dt_str, format)
