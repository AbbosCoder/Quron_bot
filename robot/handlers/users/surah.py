from aiogram import types
from loader import dp
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from aiogram.utils.markdown import hide_link

@dp.callback_query_handler(lambda call: call.data == "surahs")
async def show_surahs(call: CallbackQuery):
    """Suralar ro'yxatini ko'rsatish."""
    await call.answer()
    response = requests.get("https://api.alquran.cloud/v1/surah")
    if response.status_code == 200:
        data = response.json().get("data", [])
        keyboard = InlineKeyboardMarkup()
        for surah in data[:10]:
            keyboard.add(InlineKeyboardButton(
                f"{surah['number']}. {surah['englishName']} ({surah['name']})",
                callback_data=f"surah_{surah['number']}_1"
            ))
        keyboard.add(InlineKeyboardButton("➡️", callback_data="page_2"))
        keyboard.add(InlineKeyboardButton("🔙 Qaytish", callback_data="start"))
        await call.message.edit_text("Suralar ro'yxati (1-10):", reply_markup=keyboard)
    else:
        await call.message.answer("Suralarni olishda xatolik yuz berdi.")

@dp.callback_query_handler(lambda call: call.data.startswith("page_"))
async def paginate_surahs(call: CallbackQuery):
    """Suralar ro'yxatini sahifalash."""
    await call.answer()
    page = int(call.data.split("_")[1])
    response = requests.get("https://api.alquran.cloud/v1/surah")
    if response.status_code == 200:
        data = response.json().get("data", [])
        offset = (page - 1) * 10
        keyboard = InlineKeyboardMarkup()
        for surah in data[offset:offset + 10]:
            keyboard.add(InlineKeyboardButton(
                f"{surah['number']}. {surah['englishName']} ({surah['name']})",
                callback_data=f"surah_{surah['number']}_{page}"
            ))
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"page_{page - 1}"))
        if offset + 10 < len(data):
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"page_{page + 1}"))
        keyboard.add(*nav_buttons)
        keyboard.add(InlineKeyboardButton("🔙 Qaytish", callback_data="start"))
        await call.message.edit_text(f"Suralar ro'yxati ({offset + 1}-{offset + len(data[offset:offset + 10])}):",
                                     reply_markup=keyboard)
    else:
        await call.message.answer("Suralarni olishda xatolik yuz berdi.")

@dp.callback_query_handler(lambda call: call.data.startswith("surah_"))
async def show_surah_details(call: CallbackQuery):
    """Tanlangan sura haqida ma'lumot."""
    await call.answer()
    _, surah_number, page = call.data.split("_")
    offset = 0
    response = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_number}")
    if response.status_code == 200:
        data = response.json().get("data", {})
        data2 = data.get("ayahs", [])
        keyboard = InlineKeyboardMarkup(row_width=5)
        for ayah in data2[offset:offset + 20]:
            keyboard.insert(InlineKeyboardButton(
                f"{ayah['numberInSurah']}",
                callback_data=f"ayah_detail_{ayah['number']}"
            ))
        nav_buttons = []
        if offset + 20 < len(data2):
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"ayahs_{surah_number}_2"))
        if nav_buttons:
            keyboard.add(*nav_buttons)
        surah_name = data.get("englishName")
        ayah_count = data.get("numberOfAyahs")
        revelation_type = data.get("revelationType")

        text = (f"<blockquote>🕋 Sura: {surah_name}\n"
                f"📍 Nozil bo'lgan joy: {revelation_type}\n"
                f"🔢 Oyatlar soni: {ayah_count} </blockquote>\n\n"
                f"Oyatlar {offset + 1}-{offset + len(data2[offset:offset + 20])}:")
           
        keyboard.add(InlineKeyboardButton("🔙 Qaytish", callback_data=f"page_{page}"))
        await call.message.edit_text(text, reply_markup=keyboard) 
    else:
        await call.message.answer("Sura haqida ma'lumot olishda xatolik yuz berdi.")

@dp.callback_query_handler(lambda call: call.data.startswith("ayahs_"))
async def show_ayahs(call: CallbackQuery):
    """Suraning oyatlarini ko'rsatish."""
    await call.answer()
    _, surah_number, page = call.data.split("_")
    page = int(page)
    offset = (page - 1) * 20
    response = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_number}")
    if response.status_code == 200:
        data = response.json().get("data", {})
        data2 = data.get("ayahs", [])
        keyboard = InlineKeyboardMarkup(row_width=5)
        for ayah in data2[offset:offset + 20]:
            keyboard.insert(InlineKeyboardButton(
                f"{ayah['numberInSurah']}",
                callback_data=f"ayah_detail_{ayah['number']}"
            ))
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"ayahs_{surah_number}_{page - 1}"))
        if offset + 20 < len(data2):
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"ayahs_{surah_number}_{page + 1}"))
        if nav_buttons:
            keyboard.add(*nav_buttons)
        surah_name = data.get("englishName")
        ayah_count = data.get("numberOfAyahs")
        revelation_type = data.get("revelationType")

        text = (f"<blockquote>🕋 Sura: {surah_name}\n"
                f"📍 Nozil bo'lgan joy: {revelation_type}\n"
                f"🔢 Oyatlar soni: {ayah_count} </blockquote>\n\n"
                f"Oyatlar {offset + 1}-{offset + len(data2[offset:offset + 20])}:")
            
        keyboard.add(InlineKeyboardButton("🔙 Qaytish", callback_data=f"page_{int(surah_number)//10+1}"))
        await call.message.edit_text(text, reply_markup=keyboard)
    else:
        await call.message.answer("Oyatlarni olishda xatolik yuz berdi.")

@dp.callback_query_handler(lambda call: call.data.startswith("ayah_detail_"))
async def show_ayah_detail(call: CallbackQuery):
    """Tanlangan oyat tafsilotlari."""
    ayah_number = call.data.split("_")[2]
    await call.answer()
    response = requests.get(f"https://api.alquran.cloud/v1/ayah/{ayah_number}/editions/quran-uthmani,uz.sodik,ar.alafasy")
    if response.status_code == 200:
        data = response.json().get("data", [])
        arabic_text = data[0]["text"]
        uzbek_translation = data[1]["text"]
        translator = data[1]["edition"]["englishName"]
        surah_name = data[0]["surah"]["name"]
        surah_english_name = data[0]["surah"]["englishName"]
        ayah_number_in_surah = data[0]["numberInSurah"]
        audio_url = data[2]["audio"]

        text = (f"🕋 <b>{surah_english_name} surasi {ayah_number_in_surah}-oyat</b>\n\n"
                f"📝 <b>Asl matn (arabcha):</b>\n"
                f"<blockquote>{arabic_text}</blockquote>\n\n"
                f"🌍 <b>Tarjimasi:</b>\n"
                f"<blockquote>{uzbek_translation}</blockquote>\n\n"
                f"👳🏻‍♂️ <b>Tarjimon:</b> {translator}\n\n"
                f"{hide_link(url=audio_url)}")


        await call.message.answer(text, parse_mode="HTML")

    else:
        await call.message.answer("Oyat tafsilotlarini olishda xatolik yuz berdi.")

@dp.callback_query_handler(lambda call: call.data.startswith("ayah_audio_"))
async def send_ayah_audio(call: CallbackQuery):
    """Tanlangan oyatning audiosi."""
    await call.message.edit_reply_markup(reply_markup= None)
    await call.answer()
    ayah_number = call.data.split("_")[2]
    response = requests.get(f"https://api.alquran.cloud/v1/ayah/{ayah_number}/editions/quran-uthmani,ar.alafasy")
    
    if response.status_code == 200:
        data = response.json().get("data", [])
        surah_name = data[0].get("surah", {}).get("englishName")
        surah_number = data[0].get("surah", {}).get("number")
        ayah_in_surah = data[0].get("numberInSurah")
        audio_url = data[1].get("audio")  # "ar.alafasy" edition uchun

        caption = (
            f"<blockquote> 📖 Sura: {surah_name} ({surah_number})\n"
            f"🔢 Oyat: {ayah_in_surah}\n"
            f"📌 Tartib: {ayah_number}/6236\n"
            f"📚 Format: {surah_number}:{ayah_in_surah} </blockquote>"
        )
        #c = '<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>'
        await call.message.answer_audio(
            audio_url,
            caption=caption,
            parse_mode=types.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton('❌ O‘chirish', callback_data='del')]
            ])
        )
    else:
        await call.message.answer("Audio olishda xatolik yuz berdi.")

    # import asyncio
    # await asyncio.sleep(10)
    # await audio.delete()    

@dp.callback_query_handler(lambda call: call.data == "del")
async def del_audio(call: CallbackQuery):
    await call.message.delete()
    await call.answer("Audio o'chirildi!!!")
    