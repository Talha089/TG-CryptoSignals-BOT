from telegram import Update
from telegram.ext import ContextTypes


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    msg = (
        "Use /send_signal to send signals to all subscribed user"
        "\n\nChose better plan to get Invest Alert!"
        "\n /invoice 1 month "
        "\n /invoice 3 months "
        "\n /invoice 6 months "
    )

    await update.message.reply_text(msg)