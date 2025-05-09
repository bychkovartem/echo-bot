import asyncio
from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.data.settings import PROJECTS_CHAT_ID
from bot.handlers.admin.admin_info import cmd_admin
from bot.utils.logger import logger

scheduler = AsyncIOScheduler()

def setup_scheduler(bot: Bot):
    try:
        logger.info("Произвожу настройку планировщика задач...")
        scheduler.add_job(cmd_admin, CronTrigger(
                hour=0,
                minute=0,
                second=0
            ),
            args=[Message, bot, PROJECTS_CHAT_ID]
        )
        scheduler.start()
        logger.info("Планировщик задач был успешно настроен...")
    except Exception as e:
        logger.error(f"При настройке планировщика задач произошла ошибка: {str(e)}...")
