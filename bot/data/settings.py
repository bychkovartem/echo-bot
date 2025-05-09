import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
PATH_DATABASE: str = os.getenv("PATH_DATABASE")
PROJECTS_CHAT_ID: str = os.getenv("PROJECTS_CHAT_ID")
