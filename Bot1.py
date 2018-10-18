from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

def msg(bot, update):
    user = update.message.from_user
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('¿Cómo que ' + update.message.text)
    # update.message.reply_text('Enjoy this photo :3')
    # bot.sendPhoto(chat_id=update.message.chat_id, photo='https://www.diariodesevilla.es/resources/images/0001072217.jpg', caption = "El puto amo")


    return ConversationHandler.END

def start(bot, update):

    update.message.reply_text(
        'Hi! My name is Corchuelo. I will send you nice F- :D ')

    return GENDER


def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(bot, update):
    
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Su jefe no estaría orgulloso.')
    update.message.reply_text('Enjoy this photo :3')
    bot.sendPhoto(chat_id=update.message.chat_id, photo='https://www.diariodesevilla.es/resources/images/0001072217.jpg', caption = "El puto amo")


    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    print("holi")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("667088250:AAE05-aqg8MWp-YZkWfUO7tezE_Y6R6wdOA")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],

    #     states={
    #         GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],

    #         PHOTO: [MessageHandler(Filters.photo, photo),
    #                 CommandHandler('skip', skip_photo)],

    #         LOCATION: [MessageHandler(Filters.location, location),
    #                    CommandHandler('skip', skip_location)],

    #         BIO: [MessageHandler(Filters.text, bio)]
    #     },

    #     fallbacks=[CommandHandler('cancel', cancel)]
    # )
    
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(Filters.text, msg))

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