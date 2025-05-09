from aiogram import Bot, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from bot.core.bot import get_info_bot
from bot.data.settings import PATH_DATABASE
from bot.database.sqlite3 import db
from bot.middlewares.misc import GetText
from bot.utils.logger import logger


router = Router()


@router.message(Command(
        commands="admin"
    )
)
async def cmd_admin(message: Message = Message, bot: Bot = Bot, chat_id: int = None, text: GetText = GetText):
    ACTION = "cmd_admin"
    try:
        if not chat_id:
            chat_id = message.from_user.id
        else:
            ACTION = "night_stats"
        
        await bot.send_document(
            chat_id=chat_id,
            document=FSInputFile(
                path=PATH_DATABASE,
                filename="database.db"
            )
        )
        bot_info = await get_info_bot(bot)
        await bot.send_message(
            chat_id=chat_id,
            text=text.admin_info(bot_info)
        )
        if chat_id:
            logger.info("Статистика за сутки была отправлена в чат администрации")
        db.add_log_entry(
            user_id=chat_id,
            message=message.text,
            action=ACTION,
            status="COMPLETE",
            details=str(message)
        )
    except Exception as e:
        db.add_log_entry(
            user_id=chat_id,
            message=message.text,
            action=ACTION,
            status="FAILED",
            details=str(e)
        )
