from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from asgiref.sync import sync_to_async
from robot.models import TelegramUser
from loader import dp
import logging
from aiogram.types import Message
import aiohttp
from robot.models import MenuButton  # Django model
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    user_name=message.from_user.username
    
    try:    
        telegram_user, _ = await TelegramUser.objects.aget_or_create(
            full_name=message.from_user.full_name,
            username=user_name,
            user_id=message.from_user.id,
        )
    except:
        telegram_user, _ = await TelegramUser.objects.aget_or_create(
            full_name=message.from_user.full_name,
            username='Mavjud emas',
            user_id=message.from_user.id,
        )

    logging.info("New user")
    buttons = await sync_to_async(list)(MenuButton.objects.all())
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(button.title, callback_data=button.callback_data))
    
    await message.answer("Qur'on botiga xush kelibsiz! Quyidagi menyudan foydalaning:", reply_markup=keyboard)

@dp.callback_query_handler(text = 'start')
async def start_msg(call: types.CallbackQuery):
    await call.message.delete()
    buttons = await sync_to_async(list)(MenuButton.objects.all())
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(button.title, callback_data=button.callback_data))
    
    await call.message.answer("Qur'on botiga xush kelibsiz! Quyidagi menyudan foydalaning:", reply_markup=keyboard)

   
@dp.message_handler()
async def echo_msg(msg: Message):
    await msg.delete()