from aiogram import types, Dispatcher
from exceptions import InsufficientBalanceError, InvalidDataError, UserBlockedError
from models import Response

from services import (
    create_request_from_message,
    create_response_from_result,
    get_user_or_create,
    send_message,
    user_can_send_message,
)
from utils import decrease_balance


def register_routers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(get_user_balance_message, commands=["balance"])
    dp.register_message_handler(
        root_message_handler,
        content_types=[
            types.ContentType.TEXT,
            types.ContentType.PHOTO,
        ],
    )


async def start_command(message: types.Message):
    await message.reply(
        """Hello! This bot is designed for using Gemini AI. To get started, simply ask your question.
Images and text data types are supported.

To initiate a new chat session:
/start_chat_session

To stop the current chat session:
/stop_chat_session

To check your balance:
/balance

"""
    )


async def get_user_balance_message(message: types.Message):
    user = await get_user_or_create(message)
    return await message.answer(user.balance)


async def root_message_handler(message: types.Message):
    try:
        user = await get_user_or_create(message)
        await user_can_send_message(user)
        request = await create_request_from_message(message, user)
        result, history = await send_message(user, request)
        await decrease_balance(user)
        await create_response_from_result(request, result, history)
        return await message.answer(result)

    except InsufficientBalanceError as e:
        await message.reply(e.detail)
    except UserBlockedError as e:
        await message.reply(e.detail)
    except InvalidDataError as e:
        await message.reply(e.detail)
    except Exception as e:
        await message.reply("Something went wrong. Please try again later.")


async def stop_chat_session(message: types.Message):
    user = await get_user_or_create(message)
    await user.deactivate_chat_session()

    response = await Response.filter(user=user).order_by("-created_at").first()
    await response.deactivate_chat_session()
    await message.reply("Chat session deactivated")


async def start_chat_session(message: types.Message):
    user = await get_user_or_create(message)
    await user.activate_chat_session()
    await message.reply("Chat session activated")
