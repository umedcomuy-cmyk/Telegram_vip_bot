import json
from datetime import datetime, timedelta
from aiogram import Bot

SUBSCRIPTIONS_FILE = "subscriptions.json"

def load_subscriptions():
    try:
        with open(SUBSCRIPTIONS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_subscriptions(data):
    with open(SUBSCRIPTIONS_FILE, "w") as file:
        json.dump(data, file)

def add_user_subscription(user_id: int):
    subscriptions = load_subscriptions()
    expiration_date = (datetime.now() + timedelta(days=30)).isoformat()
    subscriptions[str(user_id)] = expiration_date
    save_subscriptions(subscriptions)

async def remove_expired_users(bot: Bot, vip_channel_id: int):
    subscriptions = load_subscriptions()
    now = datetime.now()
    updated = False

    for user_id, expiration in list(subscriptions.items()):
        if datetime.fromisoformat(expiration) <= now:
            try:
                await bot.ban_chat_member(vip_channel_id, int(user_id))
                await bot.unban_chat_member(vip_channel_id, int(user_id))
                del subscriptions[user_id]
                updated = True
            except Exception as e:
                print(f"Ошибка при удалении {user_id}: {e}")

    if updated:
        save_subscriptions(subscriptions)
