#!/usr/bin/env python3

import os
import json
import re
import random
import logging
import sys
import getopt

from dotenv import load_dotenv

from telegram import Update, Poll, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

def start(update: Update, context: CallbackContext):
  first_name = update.message.from_user.first_name
  last_name = update.message.from_user.last_name
  reply = f"Hello {first_name} {last_name}. Welcome to lectures Telegram Bot! See /help for a list of available commands. 🤖"

  update.message.reply_text(reply)
 
def help(update: Update, context: CallbackContext):
  update.message.reply_text(
"""
I can help create more engaging and interactive lectures! 🤖

Here's the list of available commands:

*Games:*
/quiz - ask a random question

*Survey:*
/vote - save or update your answer
/votecount - display the results and reset

*Common:*
/help - show the commands
""", parse_mode=ParseMode.MARKDOWN)

votes = { }

def vote(update: Update, context: CallbackContext):
  global votes

  vote = None
  text = update.effective_message.text[6:]
  id = update.effective_user.id

  if (re.search("yes|Yes|Y", text) != None):
    vote = True
  elif (re.search("no|No|N", text) != None):
    vote = False
  else:
    update.message.reply_text("Argument not valid. Allowed values are: `yes`, `no`, `Yes`, `No`, `Y`, `N`. Please, try again. 😞", parse_mode=ParseMode.MARKDOWN) 
    
    return

  if id in votes:
    update.message.reply_text(f"Updated your vote! 👍")
  else:
    update.message.reply_text(f"Got your vote! 👍")

  votes[id] = vote

def vote_count(update: Update, context: CallbackContext):
  global votes

  trues = 0
  falses = 0

  for id in votes:
    value = votes[id]

    if value:
      trues += 1
    else:
      falses += 1

  print(
"""📊 Here're the results!

[Yes]: {}
[No]: {}
""".format(trues, falses))

  votes = { }

quizes = json.load(open("sources/Quiz.json", "r"))

def quiz(update: Update, context: CallbackContext):
  quiz = random.choice(quizes)

  update.message.reply_poll(
    quiz["question"], 
    quiz["options"], 
    type=Poll.QUIZ,
    correct_option_id=quiz["correct_option_id"],
    explanation=quiz["explanation"],
    explanation_parse_mode=quiz["explanation_parse_mode"],
    open_period=quiz["open_period"]
  )

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
  script_name = sys.argv[0]
  script_options = sys.argv[1:]

  VERSION = "1.0.0"
  HELP = """usage: %s [OPTIONS]

  optional arguments:
    -h, --help         show this help message and exit
    -v, --version      show program's version number and exit""" % script_name

  try:
    arguments, values = getopt.getopt(script_options, "vh", [
      "version", 
      "help"
    ])

    for a, v in arguments:
      if a in ["-v", "--version"] and len(script_options) == 1:
        print(VERSION)
        sys.exit()
      if a in ["-h", "--help"] and len(script_options) == 1:
        print(HELP)
        sys.exit()

  except getopt.error as e:
    sys.exit()

  load_dotenv(".env")

  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  updater = Updater(os.environ["TOKEN"], use_context=True)

  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(CommandHandler("vote", vote))
  dp.add_handler(CommandHandler("votecount", vote_count))
  dp.add_handler(CommandHandler("quiz", quiz))
  dp.add_handler(MessageHandler(Filters.command, unknown))
  dp.add_handler(MessageHandler(Filters.text, echo))
  dp.add_error_handler(error_handler)

  updater.start_polling()

  # Runs the Telegram Bot until user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
  updater.idle()

if __name__ == "__main__":
  main()