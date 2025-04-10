import logging
import sys
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
import redis


# Настройки базы данных
DATABASE_URL = "sqlite:///bot_database.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

#redis_storage = RedisStorage.from_url("redis://127.0.0.1:6379/0")
#redis_client = redis.from_url("redis://127.0.0.1:6379/1")



load_dotenv()
# Переменная окружения для токена
TOKEN = getenv("YYANSTBOT")

# Bot
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    db.execute(text("PRAGMA foreign_keys = ON;"))
    try:
        yield db
    finally:
        db.close()
        