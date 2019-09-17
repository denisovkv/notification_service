import asyncio
import logging
from email.mime.text import MIMEText

import aiosmtplib

from source import settings

logger = logging.getLogger(__name__)


async def email_task(app):
    while True:
        try:
            current_batch = set()
            not_sent_batch = set()

            async with app['pool'].acquire() as con:
                result = await con.fetch('''
                    select *
                    from notifications
                    where is_sent = false and
                    is_deleted = false and
                    send_at < now()
                ''')

                for record in result:
                    current_batch.add(record.get('id'))

                    message = MIMEText(record.get('body'))
                    message['From'] = settings.EMAIL_SENDER_LOGIN
                    message['To'] = record.get('send_to')
                    message['Subject'] = record.get('title')

                    try:
                        await aiosmtplib.send(message, hostname=settings.EMAIL_SENDER_SMTP_HOST,
                                              port=settings.EMAIL_SENDER_SMTP_PORT, use_tls=True,
                                              username=settings.EMAIL_SENDER_LOGIN,
                                              password=settings.EMAIL_SENDER_PASSWORD)
                        logger.info(f'Message to {message["To"]} is sent')

                    except aiosmtplib.SMTPException as err:
                        not_sent_batch.add(record.get('id'))
                        logger.error(f'Error with sending message to {message["To"]}: {err}')

                await con.execute('''
                    update notifications
                    set is_sent = true
                    where id = any($1)
                ''', current_batch - not_sent_batch)

            await asyncio.sleep(delay_retry)
        except Exception as error:
            logger.critical(error)
            await asyncio.sleep(delay_retry / 2)
