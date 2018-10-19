from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import requests
import schedule
from time import time, sleep

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

def msg(bot, update):
    user = update.message.from_user
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('¿Cómo que ' + update.message.text + '?')
    # update.message.reply_text('Enjoy this photo :3')
    # bot.sendPhoto(chat_id=update.message.chat_id, photo='https://www.diariodesevilla.es/resources/images/0001072217.jpg', caption = "El puto amo")


    return ConversationHandler.END

def start(bot, update):

    update.message.reply_text(
        'Hi! My name is Corchuelo. I will send you nice F- :D ')


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def gatito(bot, update):
    url = 'https://api.thecatapi.com/v1/images/search?mime_type=jpg,png'
    r = requests.get(url)
    print(r.json()[0]['url'])
    bot.sendPhoto(chat_id=update.message.chat_id, photo=r.json()[0]['url'], caption = "Kawaii :3")

def time(bot, update,job_queue):
    job = job_queue.run_repeating(gatito, 60, context=update)

def main():
    print("holi")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("667088250:AAE05-aqg8MWp-YZkWfUO7tezE_Y6R6wdOA")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('gatito', gatito))

    dp.add_handler(MessageHandler(Filters.all, msg))

    schedule.every(1).minutes.do(gatito)
    schedule.run_pending()
    sleep(1)

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