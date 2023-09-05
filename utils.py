import schedule
import threading
import time

from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from database.crud import check_subscription_expiration, get_active_paid_users


def schedule_the_job_to_check_subscription():
    # Schedule the task to run daily
    schedule.every().day.at("10:00").do(check_subscription_expiration).tag("daily_subscription_check")

    # Start the schedule in a separate thread
    def run_schedule():
        print(f"Thread {threading.get_ident()} starting...")
        while True:
            schedule.run_pending()
            time.sleep(1)
        # print(f"Thread {threading.get_ident()} exiting...")

    # Start the scheduling thread
    scheduling_thread = threading.Thread(target=run_schedule)
    scheduling_thread.start()


# LIST_OF_ACTIVE_USERS = get_active_paid_users()  # List of user_id of authorized users
LIST_OF_ACTIVE_USERS = [6474275795]


class UnauthorizedAccess(Exception):
    def __init__(self, message="Unauthorized access denied"):
        self.message = message
        super().__init__(self.message)


def restricted(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ACTIVE_USERS:
            await update.message.reply_text("Unauthorized access denied.")
            return
        return await func(update, *args, **kwargs)

    return wrapped
