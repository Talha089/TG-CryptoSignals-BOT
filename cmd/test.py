from telegram import Update
from telegram.ext import ContextTypes

from utils import restricted


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /chat command")
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


@restricted
async def hello(update: Update) -> None:
    print("Received /hello command")
    await update.message.reply_text(f'Hello {update.effective_user.full_name} your id is {update.effective_user.id}')
