import asyncio
import threading
from aiogram import executor
from loader import dp

# Bot holatini boshqarish uchun global o'zgaruvchi
BOT_IS_RUNNING = False

# Botni ishga tushirish
def start_bot():
    global BOT_IS_RUNNING
    if BOT_IS_RUNNING:
        print("Bot already running")
        return
    print("Starting bot...")
    BOT_IS_RUNNING = True
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set it as the current event loop
    loop.create_task(_run_polling())  # Run the bot polling in the new loop

# Botni to'xtatish
def stop_bot():
    global BOT_IS_RUNNING
    if not BOT_IS_RUNNING:
        print("Bot already stopped")
        return
    print("Stopping bot...")
    BOT_IS_RUNNING = False
    loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()  # All tasks will be cancelled

async def _run_polling():
    """Aiogram pollingni boshlash."""
    try:
        await dp.start_polling()
    except Exception as e:
        print(f"Error in polling: {e}")