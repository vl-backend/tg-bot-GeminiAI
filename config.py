from dotenv import load_dotenv

load_dotenv()
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEYS = os.getenv("GEMINI_API_KEYS", "").split(",") or []

DB_URL = os.getenv("DB_URL") or "sqlite://db_data/db.sqlite3"
TG_IDS_ADMINS = os.getenv("TG_IDS_ADMINS", "").split(",") or []


if BOT_TOKEN is None:
    raise ValueError("Env variable 'BOT_TOKEN' is not set")
if GEMINI_API_KEYS is None:
    raise ValueError("Env variable 'GEMINI_API_KEYS' is not set")
