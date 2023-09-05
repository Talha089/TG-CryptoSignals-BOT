import os

from telegram import Update, Bot
from telegram.ext import ContextTypes

from database.crud import get_active_paid_users
from utils import restricted


@restricted
async def send_signals(update: Update) -> None:
    active_users_ids = get_active_paid_users()
    if not active_users_ids:
        await update.message.reply_text("No user has subscribed yet!")
    for id in active_users_ids:
        chat_id = id
        bot = Bot(token=os.environ["BOT_TOKEN"])
        message = "This is the signal message"
        await bot.send_message(chat_id=chat_id, text=message)
