import asyncio

from bot.core.bot import (
    create_bot, 
    get_info_bot
)
from bot.core.dispatcher import setup_dispatcher
from bot.core.scheduler import setup_scheduler
from bot.utils.logger import logger
from bot.data.settings import BOT_TOKEN
from bot.database.sqlite3 import db

async def main():
    dp = setup_dispatcher()
    ACTION = "run"
    try:
        bot = await create_bot(BOT_TOKEN)
        bot_info = await get_info_bot(bot)
        setup_scheduler(bot)
        logger.info(f"Запускаю бота {bot_info['first_name']} [@{bot_info['username']}]...")
        db.add_log_entry(
            user_id=bot_info['id'],
            message=None,
            action=ACTION,
            status="COMPLETE",
            details=str(bot_info)
        )
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        db.add_log_entry(
            user_id=bot_info['id'],
            message=None,
            action=ACTION,
            status="FAILED",
            details=str(e)
        )
    finally:
        logger.info(f"Завершаю работу бота {bot_info['first_name']} [@{bot_info['username']}]...")
        ACTION = "stop"
        db.add_log_entry(
            user_id=bot_info['id'],
            message=None,
            action=ACTION,
            status="COMPLETE",
            details=str(bot_info)
        )
        await bot.session.close()

if "__main__" == __name__:
    asyncio.run(main())
