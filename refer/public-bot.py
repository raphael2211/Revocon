# import os
# import random
# import logging
# from flask import Flask, request
# from telegram import Bot, Update
# from telegram.ext import Application, CommandHandler, ContextTypes
# from telegram.ext import MessageHandler, Filters

# # ========== SETTINGS ==========
# application = Application.builder().token("8477887518:AAHjv1NtRE6lQC8e4PVY8r2WZKdiJaAKQpg") # Get this from BotFather
# WEBHOOK_URL = "https://yourdomain.com/webhook"  # Only needed for webhook mode
# MODE = "POLLING"  # Change to "WEBHOOK" when you want to host online
# # ==============================

# # Logging for debugging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# # Create bot instance
# bot = Bot(token=TOKEN)

# # Flask app for webhook mode
# app = Flask(__name__)

# # Example database (replace with real DB later)
# codes_db = []

# # Generate a random code
# def generate_code():
#     return str(random.randint(100000, 999999))

# # Start command
# def start(update: Update, context: ContextTypes):
#     update.message.reply_text("Welcome! Use /buycode to purchase a code.")

# # Buy code command
# def buy_code(update: Update, context: ContextTypes):
#     # In production, you should check payment here before sending code
#     code = generate_code()
#     codes_db.append({"user_id": update.effective_user.id, "code": code})
#     update.message.reply_text(f"Your code: {code}\nThank you for your purchase!")

# # Unknown commands handler
# def unknown(update: Update, context: ContextTypes):
#     update.message.reply_text("Sorry, I didn't understand that command.")

# # Set up dispatcher
# dispatcher = Application(bot, None, workers=0)
# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(CommandHandler("buycode", buy_code))
# dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# # Webhook endpoint
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = Update.de_json(request.get_json(force=True), bot)
#     dispatcher.process_update(update)
#     return "OK"

# # Run in polling mode
# def run_polling():
#     from telegram.ext import Updater
#     updater = Updater(token=TOKEN, use_context=True)
#     updater.dispatcher.add_handler(CommandHandler("start", start))
#     updater.dispatcher.add_handler(CommandHandler("buycode", buy_code))
#     updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
#     updater.start_polling()
#     updater.idle()

# if __name__ == "__main__":
#     if MODE == "WEBHOOK":
#         bot.set_webhook(url=WEBHOOK_URL)
#         app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#     else:
#         run_polling()

# public_bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import os

# ==============================
# CONFIG
# ==============================
BOT_TOKEN = "8477887518:AAHjv1NtRE6lQC8e4PVY8r2WZKdiJaAKQpg"  # Replace with your public bot token
ADMIN_CHAT_ID = 123456789  # Replace with your Telegram user ID or admin group chat ID
PRICE_NGN = 2500

# ==============================
# START COMMAND
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💳 To purchase, please pay {PRICE_NGN} NGN to:\n\n"
        "Account Name: johnbosco\n"
        "Account Number: 1234567\n"
        "Bank: Example Opayn"
        "After payment, send your payment proof as an image here."
    )

# ==============================
# HANDLE PAYMENT PROOF
# ==============================
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"💰 Payment proof from @{user.username or user.first_name}\nUser ID: {user.id}\n\nApprove or Decline?"

    # Inline buttons for Approve / Decline
    buttons = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{user.id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"decline:{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Forward image to admin with buttons
    photo_file_id = update.message.photo[-1].file_id
    await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_file_id, caption=caption, reply_markup=reply_markup)

    await update.message.reply_text("📤 Payment proof sent! Please wait for admin approval.")

# ==============================
# HANDLE APPROVE/DECLINE
# ==============================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split(":")
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(chat_id=user_id, text="✅ Payment approved! Here is your code: CODE12345")
        await query.edit_message_caption(caption="✅ Approved and code sent.")
    elif action == "decline":
        await context.bot.send_message(chat_id=user_id, text="❌ Payment declined. Please ensure you pay the full amount.")
        await query.edit_message_caption(caption="❌ Declined due to insufficient payment.")

# ==============================
# MAIN
# ==============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()

