from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

async def create_bot(token: str) -> Bot:
    """Функция для создания экземпляра бота."""
    bot = Bot(
        token=token, 
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    return bot

async def get_info_bot(bot: Bot) -> dict:
    """Получает информацию о боте."""
    bot_get_me = await bot.get_me()
    bot_info: dict = {
        "id": bot_get_me.id,
        "is_bot": bot_get_me.is_bot,
        "first_name": bot_get_me.first_name,
        "last_name": bot_get_me.last_name,
        "username": bot_get_me.username,
        "language_code": bot_get_me.language_code,
        "is_premium": bot_get_me.is_premium,
        "added_to_attachment_menu": bot_get_me.added_to_attachment_menu,
        "can_join_groups": bot_get_me.can_join_groups,
        "can_read_all_group_messages": bot_get_me.can_read_all_group_messages,
        "supports_inline_queries": bot_get_me.supports_inline_queries,
        "can_connect_to_business": bot_get_me.can_connect_to_business,
        "has_main_web_app": bot_get_me.has_main_web_app
    }
    return bot_info
