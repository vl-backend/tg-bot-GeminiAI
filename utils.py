import aiohttp
from config import BOT_TOKEN, GEMINI_API_KEYS
from models import Response
from repository import init_db, close_db
from aiogram import types
import random


async def on_startup(_dispatcher):
    await init_db()


async def on_shutdown(_dispatcher):
    await close_db()


async def get_photo(photo: types.PhotoSize):
    file_id = photo.file_id
    file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                data = await response.json()
                file_path = data["result"]["file_path"]
                download_url = (
                    f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                )

                async with session.get(download_url) as file_response:
                    if file_response.status == 200:
                        file_content = await file_response.read()
                        return file_content


async def get_random_gemini_token():
    keys = GEMINI_API_KEYS
    return random.choice(keys)


async def get_chat_history(user):
    latest_response = await Response.filter(user=user).order_by("-created_at").first()
    if latest_response and latest_response.is_active_chat_session:
        history = latest_response.additional_data
        return history
    return []


async def decrease_balance(user):
    user.balance -= 1
    await user.save()
