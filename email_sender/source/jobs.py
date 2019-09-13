import asyncio
import logging
from typing import Any, MutableMapping

from source.data_utils import send_email

logger = logging.getLogger(__name__)


async def email_task(app: MutableMapping[str, Any], delay_retry: int = 60):
    while True:
        try:
            await send_email(app)
            await asyncio.sleep(delay_retry)
        except Exception as error:
            logger.critical(f'Критическая ошибка в задаче: {error}')
            await asyncio.sleep(delay_retry / 2)
