from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import aiohttp
from datetime import datetime
from loader import dp
from aiogram.types import Message

PRAYER_API_URL = "https://api.aladhan.com/v1/timingsByCity"

# Hududlar ro'yxati
LOCATIONS = [
    {"title": "Tashkent", "callback": "prayer_Tashkent"},
    {"title": "Andijan", "callback": "prayer_Andijan"},
    {"title": "Samarkand", "callback": "prayer_Samarkand"},
    {"title": "Fergana", "callback": "prayer_Fergana"},
    {"title": "Namangan", "callback": "prayer_Namangan"},
    {"title": "Bukhara", "callback": "prayer_Bukhara"},
    {"title": "Nukus", "callback": "prayer_Nukus"},
    {"title": "Urgench", "callback": "prayer_Urgench"},
    {"title": "Qarshi", "callback": "prayer_Qarshi"},
    {"title": "Jizzakh", "callback": "prayer_Jizzakh"},
    {"title": "Guliston", "callback": "prayer_Guliston"},
    {"title": "Termez", "callback": "prayer_Termez"},
    {"title": "Shahrisabz", "callback": "prayer_Shahrisabz"},
    {"title": "Qo'qon", "callback": "prayer_Qoqon"},
    {"title": "Navoi", "callback": "prayer_Navoi"},
    {"title": "Zarafshan", "callback": "prayer_Zarafshan"}
]


async def generate_locations_keyboard():
    """Hududlarni tanlash uchun InlineKeyboard yaratadi"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    for location in LOCATIONS:
        keyboard.insert(InlineKeyboardButton(location["title"], callback_data=location["callback"]))
    return keyboard



# Namoz vaqtlarini olish tugmalar bilan
@dp.callback_query_handler(text = 'namoz')
async def start_command(call: CallbackQuery):
    keyboard = await generate_locations_keyboard()
    await call.answer()
    await call.message.edit_text("Hududingizni tanlang:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == "prayer_back")
async def back_to_locations(call: CallbackQuery):
    keyboard =  await generate_locations_keyboard()
    await call.answer()
    await call.message.edit_text("Hududingizni tanlang:", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data.startswith("prayer_"))
async def get_prayer_times(call: CallbackQuery):
    location = call.data.split("_")[1]
    await call.answer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{PRAYER_API_URL}?city={location}&country=Uzbekistan") as response:
            if response.status == 200:
                data = await response.json()
                timings = data["data"]["timings"]
                last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                keyboard = InlineKeyboardMarkup(row_width=1)
                keyboard.add(
                    InlineKeyboardButton("🔄 Yangilash", callback_data=f"prayer_{location}"),
                    InlineKeyboardButton("🔙 Qaytish", callback_data="start"),
                )
                m = await call.message.edit_text(
                            f"📍 <b>{location} hududi namoz vaqtlari:</b>\n\n"
                            f"🌅 <b>Bomdod:</b> <code>{timings['Fajr']}</code>\n"
                            f"☀️ <b>Quyosh:</b> <code>{timings['Sunrise']}</code>\n"
                            f"🌞 <b>Peshin:</b> <code>{timings['Dhuhr']}</code>\n"
                            f"🌤 <b>Asr:</b> <code>{timings['Asr']}</code>\n"
                            f"🌇 <b>Shom:</b> <code>{timings['Maghrib']}</code>\n"
                            f"🌌 <b>Xufton:</b> <code>{timings['Isha']}</code>\n\n"
                            f"🕰 <i>So'nggi yangilanish:</i> {last_updated}",
                            reply_markup=keyboard,
                        )
                await m.pin()

            else:
                await call.message.answer("Namoz vaqtlarini olishda xatolik yuz berdi.")



