from aiogram import types
from client import GeminiAIClient
from config import TG_IDS_ADMINS
from enums import GeminiModelEnum
from exceptions import InsufficientBalanceError, UserBlockedError
from models import Request, Response, User
from utils import get_chat_history, get_photo, get_random_gemini_token


async def get_user_or_create(message: types.Message):
    user, _created = await User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "username": message.from_user.username,
        },
    )
    return user


async def user_can_send_message(user: User):
    if user.telegram_id in TG_IDS_ADMINS:
        return
    elif not user.is_active:
        raise UserBlockedError

    elif user.balance == 0:
        raise InsufficientBalanceError


async def send_message(user: User, req):
    token = await get_random_gemini_token()
    if req.image_data:
        gemini = GeminiAIClient(token, GeminiModelEnum.GEMINI_PRO_VISION.value)
        result = await gemini.send_message(req)
        return result, None
    else:
        history = await get_chat_history(user)
        gemini = GeminiAIClient(
            token, GeminiModelEnum.GEMINI_PRO.value, chat_history=history
        )
        result = await gemini.send_message(req)
        return result, gemini.chat_history


async def create_request_from_message(message, user):
    data = {"user": user}
    if message.text:
        data["query"] = message.text
    elif message.caption:
        data["query"] = message.caption

    if message.photo:
        photo = await get_photo(message.photo[-1])
        data["image_data"] = photo
    request = await Request.create(**data)
    return request


async def create_response_from_result(request, result, history):
    data = {
        "user": request.user,
        "request": request,
        "content": result,
    }
    if history:
        data["is_active_chat_session"] = True
        data["additional_data"] = history
    response = await Response.create(**data)
    return response
