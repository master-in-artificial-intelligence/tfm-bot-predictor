#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import requests, logging, json

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    message = "Hey there!, I can predict results for tennis matches! What? you don't believe me? launch the /prediction command and you will see :P"
    update.message.reply_text()


def help(update, context):
    """Send a message when the command /help is issued."""
    message = "If you want to get next predicions available just launch the /prediction command and I will do the rest"
    update.message.reply_text(message)

def prediction(update, context):
    """Starts the prediction process!!"""
    req = requests.get('http://localhost:5000/predictions')
    status_code = req.status_code
    update.message.reply_text('Here are the predictions :)')

    message = ''
    json_response = json.loads(req.text)
    for key in json_response:
        for match in json_response[key]:
            message += 'Match: ' + match['homePlayer'] + ' - ' + match['awayPlayer'] + '\n'
            message += 'Date: ' + match['date'] + '\n'
            message += 'Predicted winner: ' + match['predictedWinner'] + '\n'
            message += 'Probability: ' + match['predictionProbability'] + '\n'
            message += '------------\n'

    update.message.reply_text(message)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    print('Bot started')
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1869868845:AAGYUApFhRJw_IKBICTpEu8cpYTls-reMQk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("prediction", prediction))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

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