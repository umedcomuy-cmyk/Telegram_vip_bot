from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, VIP_CHANNEL_ID
from datetime import datetime, timedelta
import json
import os

ACCESS_FILE = 'access.json'

def setup_handlers(dp, bot):
    @dp.message(commands=['start'])
    async def start_handler(message: types.Message):
        first_name = message.from_user.first_name
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🚪 Запросить доступ', callback_data='request_access')],
            [InlineKeyboardButton(text='💳 Оплатить картой (СПБ, ЮKassa)', callback_data='pay_card')],
            [InlineKeyboardButton(text='💰 Оплатить криптовалютой', callback_data='pay_crypto')]
        ])
        await message.answer(
            f"🏢 Добро пожаловать в YUKI CORPORATION — ваш инвестиционный ассистент!\n\n"
            f"👋 Привет, {first_name}!\n\n"
            f"Вы находитесь в официальном боте YUKI CORPORATION.\n"
            f"Здесь вы сможете оформить доступ в наш закрытый VIP-канал, где публикуются торговые сигналы, прогнозы и аналитика по рынкам.\n\n"
            f"💎 Что входит в VIP-доступ (всего за $20/мес):\n"
            f"📊 Торговые сигналы по золоту (XAU/USD), NASDAQ и мажорным валютным парам\n"
            f"📰 Ежедневные обзоры ключевых новостей рынка\n"
            f"📈 Прогнозы движения цены с рекомендациями по входу/выходу\n"
            f"💰 Практические стратегии управления рисками\n"
            f"📑 Отчёты по сделкам для инвесторов\n\n"
            f"⚠️ Важно: VIP-канал работает в одностороннем режиме.\n"
            f"Вы будете получать только проверенный контент — без лишнего шума и переписок.\n\n"
            f"📌 Как получить доступ к VIP-каналу?\n"
            f"1️⃣ Нажмите кнопку ниже и отправьте заявку\n"
            f"2️⃣ После одобрения получите персональную ссылку для входа\n"
            f"3️⃣ Начнёте получать актуальные сигналы и аналитику",
            reply_markup=keyboard
        )

    @dp.callback_query(lambda c: c.data == 'request_access')
    async def handle_request_access(callback: types.CallbackQuery):
        user = callback.from_user
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='✅ Одобрить', callback_data=f'approve_{user.id}')]
        ])
        await bot.send_message(
            ADMIN_ID,
            f"📥 Новый запрос на доступ:\n\n"
            f"👤 Пользователь: {user.full_name} (@{user.username})\n"
            f"🆔 Telegram ID: {user.id}\n\n"
            f"Нажмите, чтобы одобрить:",
            reply_markup=keyboard
        )
        await callback.answer("Заявка отправлена. Ожидайте одобрения.")

    @dp.callback_query(lambda c: c.data.startswith('approve_'))
    async def approve_user(callback: types.CallbackQuery):
        user_id = int(callback.data.split('_')[1])
        try:
            await bot.send_message(user_id, f"✅ Доступ одобрен! Вот ссылка на VIP-канал: https://t.me/YukiSupport_bot")
            await bot.send_message(callback.from_user.id, "Пользователь получил доступ.")
            save_access(user_id)
        except Exception as e:
            await bot.send_message(callback.from_user.id, f"Ошибка при отправке сообщения: {e}")

    @dp.callback_query(lambda c: c.data == 'pay_card')
    async def pay_card(callback: types.CallbackQuery):
        await callback.message.answer(
            "💳 Оплата банковской картой:\n\n"
            "1️⃣ Переведите $20 на карту:\n"
            "`4276 3801 2345 6789`\n\n"
            "2️⃣ Отправьте скриншот чека сюда👇"
        )
        await callback.answer()

    @dp.message(lambda message: message.photo)
    async def handle_receipt(message: types.Message):
        if message.caption:
            caption = message.caption
        else:
            caption = f"🧾 Чек от @{message.from_user.username} (ID: {message.from_user.id})"
        await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=caption)
        await message.reply("✅ Чек получен! Мы проверим и вскоре свяжемся с вами.")

def save_access(user_id):
    data = {}
    if os.path.exists(ACCESS_FILE):
        with open(ACCESS_FILE, 'r') as f:
            data = json.load(f)
    data[str(user_id)] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    with open(ACCESS_FILE, 'w') as f:
        json.dump(data, f)
