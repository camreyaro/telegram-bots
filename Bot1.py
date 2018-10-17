from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Corchuelo. I will send you nice F- :D '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

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
    bot.sendPhoto(chat_id=update.message.chat_id, photo='data:image/jpeg;base64,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', caption = "El puto amo")


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
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("667088250:AAE05-aqg8MWp-YZkWfUO7tezE_Y6R6wdOA")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )


    dp.add_handler(conv_handler)

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