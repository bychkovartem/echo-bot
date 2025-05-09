from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database.sqlite3 import db
from bot.middlewares.misc import GetText

router = Router()

@router.message(
    Command(
        commands="help",
        ignore_case=True
    )
)
async def cmd_help(message: Message, text: GetText = GetText):
    ACTION = "cmd_help"
    try:
        user_id = message.from_user.id
        await message.answer(
            text=text.help()
        )
        db.add_log_entry(
            user_id=user_id,
            message=message.text,
            action=ACTION,
            status="COMPLETE",
            details=str(message)
        )
    except Exception as e:
        db.add_log_entry(
            user_id=user_id,
            message=message.text,
            action=ACTION,
            status="FAILED",
            details=str(e)
        )
