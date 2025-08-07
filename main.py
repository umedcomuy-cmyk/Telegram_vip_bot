from handlers import setup_handlers
from aiogram import Bot, Dispatcher, types
import asyncio
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher()

setup_handlers(dp, bot)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
