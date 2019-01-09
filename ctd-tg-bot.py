#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from datetime import datetime
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TALIS = {"Ecker": "Eckertalsperre",
         "Grane": "Granetalsperre",
         "Innerste": "Innerstetalsperre",
         "Oder": "Odertalsperre",
         "Oker": "Okertalsperre",
         "Soese": "Sösetalsperre"}


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Hallo, i bims 1 Talsperrenbot"""
    update.message.reply_text("""Hallo, ich bin ein Bot.
Ich liefere tolle Informationen über die Talsperren der Harzwasserwerke. Die Infos kommen von
https://www.harzwasserwerke.de/infoservice/aktuelle-talsperrendaten""")


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""Commands:"""
                              """/current - Aktuelle Daten der gegebenen Talsperre (default = Eckertalsperre)"""
                              """/help - Hilfetext mit allen Commands""", parse_mode=ParseMode.MARKDOWN)


def current(bot, update, args):
    """Responds with current resevoir data"""
    if not args:
        which = "Ecker"
    else:
        for arg in args:
            if arg in TALIS:
                which = arg
                break

    url = "https://angercloud.pro/ctd/static/%s.json" % which
    request = requests.get(url)
    request.encoding = 'utf-8'
    data = request.json()
    current_data = max(data["data"], key=lambda k: k['date'])

    message = "Aktuelle Daten der %s (%s):\n" \
              "Stauinhalt: %.2f\n" \
              "Füllgrad: %.2f\n" \
              "Zufluss: %.2f\n" \
              "Abfluss: %.2f" % (
                  TALIS[which], datetime.utcfromtimestamp(current_data["date"] / 1000), current_data["stauinhalt"],
                  current_data["fuellgrad"], current_data["zufluss"], current_data["abfluss"])

    update.message.reply_text(message)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    token = open("token").read()
    updater = Updater(token.strip())

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("current", current, pass_args=True))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
