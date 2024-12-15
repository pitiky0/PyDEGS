import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dotenv
import logging
from template.reset_password_email import get_html_body, get_text_body
from template.verification_email import get_formated_text, get_formated_html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

APP_NAME = os.getenv("APP_NAME")
AUTH_SERVICE = os.getenv("AUTH_SERVICE_EMAIL")
FRONTEND_URL = os.getenv("FRONTEND_URL")
SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
VERIFICATION_SUBJECT = os.getenv("VERIFICATION_SUBJECT", "Email Verification from {app_name}")
PASSWORD_RESET_SUBJECT = os.getenv("PASSWORD_RESET_SUBJECT", "Password Reset")

def send_email(subject, body_text, body_html, recipient):
    # Create a multipart message
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"{APP_NAME}<{SENDER}>"
    msg["To"] = recipient

    # Create plain text version of the email
    text_part = MIMEText(body_text, "plain")
    msg.attach(text_part)

    # Create HTML version of the email
    html_part = MIMEText(body_html, "html")
    msg.attach(html_part)

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
            smtp_server.login(SENDER, PASSWORD)
            smtp_server.sendmail(from_addr=SENDER, to_addrs=recipient, msg=msg.as_string())
            logger.info(f"Email successfully sent to {recipient}")
    except Exception as e:
        logger.info(f"Failed to send email to {recipient}. Error: {e}")

def send_verification_email(email, token):
    try:
        body_html = get_formated_html(app_name=APP_NAME, email=email, token=token, auth_service=FRONTEND_URL)
        body_text = get_formated_text(app_name=APP_NAME, email=email, token=token, auth_service=FRONTEND_URL)
    except Exception as e:
        logger.info(f"Failed to format email body. Error: {e}")
        return

    subject = VERIFICATION_SUBJECT.format(app_name=APP_NAME)
    send_email(subject, body_text, body_html, email)

def send_password_reset_email(email, token):
    try:
        body_text = get_text_body(app_name=APP_NAME, auth_service=FRONTEND_URL, token=token, email=email)
        body_html = get_html_body(app_name=APP_NAME, auth_service=FRONTEND_URL, token=token, email=email)
    except Exception as e:
        logger.info(f"Failed to format email body. Error: {e}")
        return

    subject = PASSWORD_RESET_SUBJECT
    send_email(subject, body_text, body_html, email)