from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.sqlite3 import db
from bot.middlewares.misc import GetText

router = Router()

@router.message(
    CommandStart(
        ignore_case=True
    )
)
async def cmd_start(message: Message, text: GetText = GetText):
    ACTION = "cmd_start"
    try:
        user_id = message.from_user.id
        if not db.user_exists(user_id):
            db.add_user(
                user_id=user_id,
                is_bot=message.from_user.is_bot,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
                is_premium=message.from_user.is_premium,
                added_to_attachment_menu=message.from_user.added_to_attachment_menu,
                can_join_groups=message.from_user.can_join_groups,
                can_read_all_group_messages=message.from_user.can_read_all_group_messages,
                supports_inline_queries=message.from_user.supports_inline_queries,
                can_connect_to_business=message.from_user.can_connect_to_business,
                has_main_web_app=message.from_user.has_main_web_app,
                admin=0
            )
        await message.answer(
            text=text.start()
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
