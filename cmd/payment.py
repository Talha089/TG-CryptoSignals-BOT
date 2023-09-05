import os

from telegram import LabeledPrice, Update
from telegram.ext import ContextTypes
from database.crud import create_payment_record
from dotenv import load_dotenv
load_dotenv()

PAYMENT_PROVIDER_TOKEN = os.environ["STRIP_TEST_TOKEN"]


async def create_invoice(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends an invoice without shipping-payment."""
    global price
    duration = None
    chat_id = update.message.chat_id
    text = update.message.text

    title = "Payment Example"
    description = "Payment Example for Python-Telegram-Bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "USD"
    # price in dollars
    if "1 month" in text:
        duration = "1 month"
        context.user_data['duration'] = duration
        price = 10  # Adjust the price for 1 month subscription
    elif "3 months" in text:
        duration = "3 months"
        context.user_data['duration'] = duration
        price = 25  # Adjust the price for 3 months subscription
    elif "6 months" in text:
        duration = "6 months"
        context.user_data['duration'] = duration
        price = 45  # Adjust the price for 6 months subscription
    else:
        await update.message.reply_text("Invalid subscription duration. Please choose 1 month, 3 months, or 6 months.")
        return

    # Store the duration in the context for later use
    print("duration in invoice --------------------------->: ",duration)


    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
    )


# after payment, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # Retrieve the duration from the context
    duration = context.user_data.get('duration')
    print("duration in success --------------------------->: ",duration)

    # Extract information about the successful payment from the update
    payment_info = update.message.successful_payment

    # This is the Telegram-specific identifier for the payment charge. It is a unique identifier associated with the payment transaction within Telegram's payment system.
    tele_payment_id = payment_info.telegram_payment_charge_id

    # This is the identifier provided by the external payment provider (e.g., Stripe, PayPal) for the payment charge.
    prov_payment_id = payment_info.provider_payment_charge_id
    chat_id = update.message.chat_id
    full_name = update.effective_user.full_name
    # The user has paid the expected amount in the expected currency You can now perform actions such as updating a database, sending a confirmation, etc.

    # Store data in db
    create_payment_record(full_name=full_name, chat_id=str(chat_id), payed_id=prov_payment_id, package_plan=duration)

    await update.message.reply_text(
        f"Thank you for your payment! \n telegram_payment_charge_id: {tele_payment_id} and provider_payment_charge_id: {prov_payment_id}")
