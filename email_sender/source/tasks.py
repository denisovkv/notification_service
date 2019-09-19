import logging
from email.mime.text import MIMEText

import aiosmtplib

from source import settings

logger = logging.getLogger(__name__)


async def confirm_sending(notification_id):
    pass


async def email_task(**kwargs):

    message = MIMEText(kwargs.get('body'))
    message['From'] = settings.EMAIL_SENDER_LOGIN
    message['To'] = kwargs.get('send_to')
    message['Subject'] = kwargs.get('title')

    try:
        await aiosmtplib.send(message, hostname=settings.EMAIL_SENDER_SMTP_HOST,
                              port=settings.EMAIL_SENDER_SMTP_PORT, use_tls=True,
                              username=settings.EMAIL_SENDER_LOGIN,
                              password=settings.EMAIL_SENDER_PASSWORD)
        logger.info(f'Message to {message["To"]} is sent')

        await confirm_sending(kwargs['id'])

    except aiosmtplib.SMTPException as err:
        logger.error(f'Error with sending message to {message["To"]}: {err}')
