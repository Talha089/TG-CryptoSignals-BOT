import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from cmd.payment import create_invoice, precheckout_callback, successful_payment_callback
from cmd.signals import send_signals
from cmd.start_help import start_callback
from cmd.test import get_chat_id, hello
from utils import schedule_the_job_to_check_subscription
from dotenv import load_dotenv
load_dotenv()

bot_token = os.environ["BOT_TOKEN"]

schedule_the_job_to_check_subscription()


def main():
    print("Starting the bot application")

    app = ApplicationBuilder().token(bot_token).build()
    print("Adding command handler")
    app.add_handler(CommandHandler("start", start_callback))
    app.add_handler(CommandHandler("help", start_callback))
    app.add_handler(CommandHandler("send_signal", send_signals))
    app.add_handler(CommandHandler("invoice", create_invoice))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )
    app.add_handler(CommandHandler("chat", get_chat_id))
    app.add_handler(CommandHandler("hello", hello))

    print("Running the bot Application")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
