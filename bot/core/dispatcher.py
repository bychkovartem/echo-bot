from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import (
    start,
    help
)
from bot.handlers.user import (
    echo
)
from bot.handlers.admin import (
    admin_info
)
from bot.utils.logger import logger

storage = MemoryStorage()

def setup_dispatcher():
    try:
        logger.info("Произвожу настройку диспетчера...")
        dp = Dispatcher(storage=storage)
        dp.include_routers(
            start.router,
            help.router,

            admin_info.router,

            echo.router
        )
        logger.info("Диспетчер был успешно настроен...")
        return dp
    except Exception as e:
        logger.error(f"При настройке диспетчера произошла ошибка: {str(e)}...")
