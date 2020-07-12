import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

def start(update: Update, context: CallbackContext):
  first_name = update.message.from_user.first_name
  last_name = update.message.from_user.last_name
  reply = f"Hello {first_name} {last_name}. Welcome to lectures Telegram Bot! See /help for a list of available commands. 🤖"

  update.message.reply_text(reply)
 
def help(update: Update, context: CallbackContext):
  update.message.reply_text("Need some Help?")

def unknown(update: Update, context: CallbackContext):
  update.message.reply_text("Sorry, I can't understand that. See /help for a list of available commands. 😭")

def echo(update: Update, context: CallbackContext):
  first_name = update.message.from_user.first_name
  last_name = update.message.from_user.last_name
  message = update.message.text[0].lower() + update.message.text[1:]

  print(f"💬 {first_name} {last_name} asks: {message}")

def error_handler(update: Update, context: CallbackContext):
  print(f"😱 Telegram_Bot.py::error_handler - An exception was raised while handling an update.")

def main():
  load_dotenv(".env")

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  updater = Updater(os.environ["TOKEN"], use_context=True)

  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  dp.add_handler(MessageHandler(Filters.text, echo))
  dp.add_error_handler(error_handler)

  updater.start_polling()

  # Runs the Telegram Bot until user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
  updater.idle()

if __name__ == "__main__":
  main()