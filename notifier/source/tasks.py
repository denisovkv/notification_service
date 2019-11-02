import logging
import smtplib

from aiohttp import ClientSession
from email.message import EmailMessage

from app import settings

logger = logging.getLogger(__name__)


def confirm_sending(notification_id):
    async with ClientSession() as session, session.get(f'{settings.BACKEND_CONFIRM_ENDPOINT}/{notification_id}'):
        pass


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

    except smtplib.SMTPException:
        logger.error(f'Error with sending message: {payload}')
