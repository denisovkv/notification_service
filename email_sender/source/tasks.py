import logging
import smtplib

from email.message import EmailMessage

import requests

from source import settings

logger = logging.getLogger(__name__)


def confirm_sending(notification_id):
    requests.patch(f'{settings.DB_WRITER_CONFIRM_ENDPOINT}/{notification_id}',
                   json={'is_sent': True})


def send_email(payload):

    message = EmailMessage()
    message['From'] = settings.EMAIL_SENDER_LOGIN
    message['To'] = payload.get('send_to')
    message['Subject'] = payload.get('title')
    message.set_content(payload.get('body'))

    try:
        with smtplib.SMTP_SSL(
                host=settings.EMAIL_SENDER_SMTP_HOST,
                port=settings.EMAIL_SENDER_SMTP_PORT
        ) as s:
            s.login(settings.EMAIL_SENDER_LOGIN, settings.EMAIL_SENDER_PASSWORD)
            s.send_message(message)

        confirm_sending(payload['id'])

    except smtplib.SMTPException:
        logger.error(f'Error with sending message: {payload}')
