from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

import logging

def start(update: Update, context: CallbackContext):
  update.message.reply_text('Welcome!')
 
def help(update: Update, context: CallbackContext):
  update.message.reply_text("Need some Help?")

def unknown(update: Update, context: CallbackContext):
  update.message.reply_text("Sorry, I didn't understand that Command.")

def main():
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  updater = Updater("XXX", use_context=True)

  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(MessageHandler(Filters.command, unknown))

  updater.start_polling()

  # Runs the Telegram Bot until user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
  updater.idle()

  pass

if __name__ == "__main__":
  main()