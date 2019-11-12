import logging
import smtplib
from email.message import EmailMessage

import requests
from app import settings

logger = logging.getLogger(__name__)


def confirm_sending(notification_id):
    requests.patch(f'{settings.BACKEND_CONFIRM_ENDPOINT}/{notification_id}')


def send_email(payload):

    message = EmailMessage()
    message['From'] = settings.NOTIFIER_LOGIN
    message['To'] = payload.get('send_to')
    message['Subject'] = payload.get('title')
    message.set_content(payload.get('body'))

    try:
        with smtplib.SMTP_SSL(
                host=settings.NOTIFIER_SMTP_HOST,
                port=settings.NOTIFIER_SMTP_PORT
        ) as s:
            s.login(settings.NOTIFIER_LOGIN, settings.NOTIFIER_PASSWORD)
            s.send_message(message)

        confirm_sending(payload['id'])

    except smtplib.SMTPException as er:
        logger.error(f'Error with sending message {payload}: {er}')
