from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required")

WEBHOOK_SECRET = getenv("WEBHOOK_SECRET", "")
DATABASE_PATH = getenv("DATABASE_PATH", "data.sqlite")
WEBHOOK_PORT = int(getenv("WEBHOOK_PORT", "8080"))
