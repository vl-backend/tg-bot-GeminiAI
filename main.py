from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN
from utils import on_shutdown, on_startup
from routers import register_routers


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
register_routers(dp)

if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
