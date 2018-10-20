############################
# IMPORTS
############################
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
import requests
import schedule
import sqlite3
from time import time, sleep
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
# from datetime import *
# import locale
#############################
#############################

# Set locale to Spain
# locale.setlocale(locale.LC_ALL, 'es_ES')


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def msg(bot, update):
    # user = update.message.from_user
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('¿Cómo que ' + update.message.text + '?')
    # update.message.reply_text('Enjoy this photo :3')
    # bot.sendPhoto(chat_id=update.message.chat_id, photo='https://www.diariodesevilla.es/resources/images/0001072217.jpg', caption = "El puto amo")


    return ConversationHandler.END

def start(bot, update):
    global chat_id;
    chat_id = update.message.chat_id;
    print(chat_id)
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

def horario(bot,update):
    conn = sqlite3.connect('test.db')

    # day = date.today().strftime("%A")

    output = """<table>
                    <tr>
                        <th>ASIGNATURA</th>
                        <th>DIA</th>
                        <th>HORA</th>
                        <th>AULA</th>
                    </tr>"""
    # for item in conn.execute("SELECT * FROM HORARIO WHERE DIA = '" + day + "';"):
    for item in conn.execute("SELECT * FROM HORARIO;"):
        output += """<td>
                        <tr>""" + item[0] + """</tr>
                        <tr>""" + item[1] + """</tr>
                        <tr>""" + item[2] + """</tr>
                        <tr>""" + item[3] + """</tr>
                    </td>"""

    update.message.reply_text("Ahí va tu horario de hoy!")
    update.message.reply_text(chat_id=update.message.chat_id, text=output, parse_mode=telegram.ParseMode.HTML)


def gatito(bot,update):
    url = 'https://api.thecatapi.com/v1/images/search?mime_type=jpg,png'
    r = requests.get(url)
    print(r.json()[0]['url'])
    bot.sendPhoto(chat_id=update.message.chat_id, photo=r.json()[0]['url'], caption = "Kawaii :3")

def gatitoTriggered(bot):
    url = 'https://api.thecatapi.com/v1/images/search?mime_type=jpg,png'
    r = requests.get(url)
    print(r.json()[0]['url'])
    bot.sendPhoto(chat_id=chat_id, photo=r.json()[0]['url'], caption = "Kawaii :3")

def main():
    print("holi")
    
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("667088250:AAE05-aqg8MWp-YZkWfUO7tezE_Y6R6wdOA")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('gatito', gatito))

    dp.add_handler(CommandHandler('horario', horario))

    dp.add_handler(MessageHandler(Filters.all, msg))

    scheduler = BackgroundScheduler()

    trigger = CronTrigger(year='*', month='*', day='*', hour='*', minute='02', second='00')

    scheduler.add_job(gatitoTriggered, trigger=trigger, args=(updater.bot,))

    scheduler.start()

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